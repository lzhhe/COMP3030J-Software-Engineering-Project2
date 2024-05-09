from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from random import random

from collections import defaultdict

import numpy as np
import pandas as pd
from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sklearn.cluster import KMeans
from sqlalchemy import and_, or_
from statsmodels.tsa.arima.model import ARIMA
from werkzeug.security import generate_password_hash, check_password_hash

from .views_utils import *

from .models import *

government = Blueprint('government', __name__, url_prefix='/government')  # government is name of blueprint


@government.route('/')
def index():
    return render_template('government/index.html')


def buildKmeansDataset():
    orders = Order.query.filter(Order.orderStatus == "FINISHED").all()
    dataset = defaultdict(list)

    for order in orders:
        waste_type_name = order.wasteType.name
        weight = order.weight
        duration = (order.finishDate - order.date).days

        dataset[waste_type_name].append([weight, duration])

    print("KmeansDataset: ", dict(dataset))

    return dict(dataset)


# 显示的话看是显示所有的还是对于部门进行聚类，聚类效果可以多样
def TypeKmeansCenter(dataset, k=1):  # 聚类中心为1
    centers = {}

    for category, data in dataset.items():
        # 将数据列表转换为 NumPy 数组，以适应 KMeans
        data_array = np.array(data)

        if len(data_array) >= k:
            # 进行 KMeans 聚类
            model = KMeans(n_clusters=k)
            model.fit(data_array)
            centers[category] = model.cluster_centers_
        else:
            centers[category] = np.array([])

    return centers


@government.route('/build_kmeans')
def build_kmeans():
    dataset = buildKmeansDataset()
    centers = TypeKmeansCenter(dataset)
    centers = {category: center.tolist() for category, center in centers.items()}
    print("KMeans Centers:", centers)
    return jsonify({'dataset': dataset, 'centers': centers})


def generate_array():
    current_date = datetime.now().date()
    date_values = [[current_date - timedelta(days=i), 0.0] for i in range(30)]
    return date_values


def buildWeightDataset():
    # 获取最近30天内的订单数据
    thirty_days_ago = datetime.now() - timedelta(days=30)
    orders = Order.query.filter(Order.orderStatus == "FINISHED", Order.date >= thirty_days_ago).all()
    dataset = defaultdict(list)
    dateList = generate_array()  # [date, 0]

    # 构建每个类别的时间序列
    for order in orders:
        waste_type_name = order.wasteType.name
        multiplier = order.multiplier
        weight = float(order.weight * multiplier)  # 将重量转换为float类型，乘以倍率
        order_date = order.date

        # 检查废物类型是否在数据集中，如果不在，则初始化为 dateList
        if waste_type_name not in dataset:
            dataset[waste_type_name] = [entry.copy() for entry in dateList]  # 深拷贝 dateList

        for entry in dataset[waste_type_name]:
            if entry[0] == order_date:
                entry[1] = entry[1] + weight
                break

    # 对每个类别的数据按日期进行排序
    for category in dataset:
        dataset[category].sort(key=lambda x: x[0])

    # print(dict(dataset))
    return dict(dataset)


def forecastWeight(dataset, days=5, order=(1, 1, 1)):
    forecasts = {}
    for category, data in dataset.items():
        # 提取每个类别的重量和日期数据
        dates = [entry[0] for entry in data]
        weights = [entry[1] for entry in data]
        df = pd.DataFrame({'Date': dates, 'Weight': weights})

        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.index.freq = 'D'
        # 应用ARIMA模型
        model = ARIMA(df, order=order, freq='D')

        fitted_model = model.fit()

        # 进行预测
        forecast = fitted_model.forecast(steps=days)
        forecast_values = forecast.values.tolist()

        forecasts[category] = forecast_values

    return forecasts


def generate_time_array():
    current_date = datetime.now().date()
    date_values = [[current_date - timedelta(days=i), []] for i in range(30)]
    return date_values


def buildTimeDataset():
    # 获取最近30天内的订单数据
    thirty_days_ago = datetime.now() - timedelta(days=30)
    orders = Order.query.filter(Order.orderStatus == "FINISHED", Order.date >= thirty_days_ago).all()
    dataset = defaultdict(list)
    dateList = generate_time_array()  # 形式为[date, []]

    # 构建每个类别的时间序列
    for order in orders:
        waste_type_name = order.wasteType.name
        order_date = order.date
        process_time = (order.finishDate - order.date).days  # 计算处理时间（天）

        # 检查废物类型是否在数据集中，如果不在，则初始化为 dateList
        if waste_type_name not in dataset:
            dataset[waste_type_name] = [entry.copy() for entry in dateList]  # 深拷贝 dateList

        for entry in dataset[waste_type_name]:
            print(entry)
            if entry[0] == order_date:
                if waste_type_name == "HEAVY_METAL_WASTEWATER":
                    print(order_date,process_time)
                entry[1].append(process_time)  # 创建新的处理时间列表并添加处理时间
                break

        print(dict(dataset))

    print(dict(dataset))
    return dict(dataset)


def forecastTime(dataset, days=5, order=(1, 1, 1)):
    forecasts = {}
    for category, data in dataset.items():
        # 提取每个类别的重量和日期数据
        dates = [entry[0] for entry in data]
        print(dates)
        times = [entry[1] for entry in data]
        print(times)
        df = pd.DataFrame({'Date': dates, 'Times': times})

        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.index.freq = 'D'
        # 应用ARIMA模型
        model = ARIMA(df, order=order, freq='D')

        fitted_model = model.fit()

        # 进行预测
        forecast = fitted_model.forecast(steps=days)
        forecast_values = forecast.values.tolist()

        forecasts[category] = forecast_values

    return forecasts


@government.route('/build_arima')
def build_arima():
    weightDataset = buildWeightDataset()
    weightForecasts = forecastWeight(weightDataset)
    weightForecasts = {category: forecast for category, forecast in weightForecasts.items()}
    # print("Weight Forecasts:", weightForecasts)

    timeDataset = buildTimeDataset()
    timeForecasts = forecastTime(timeDataset)
    timeForecasts = {category: forecast for category, forecast in timeForecasts.items()}
    print("Time Forecasts:", timeForecasts)
    return jsonify({'dataset': timeDataset, 'forecasts': weightForecasts})
