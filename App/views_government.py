from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from random import random

import numpy as np
import pandas as pd
from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sklearn.cluster import KMeans
from sqlalchemy import and_, or_
from statsmodels.tsa.arima.model import ARIMA
from werkzeug.security import generate_password_hash, check_password_hash

from .views_utils import *

government = Blueprint('government', __name__, url_prefix='/government')  # government is name of blueprint


@government.route('/')
def index():
    return render_template('government/index.html')


def buildKmeansDataset():
    orders = Order.query.filter(Order.orderStatus.name == "FINISHED").all()
    dataset = defaultdict(list)

    for order in orders:
        waste_type_name = order.wasteType.name
        weight = order.weight
        duration = (order.finishDate - order.date).days

        dataset[waste_type_name].append([weight, duration])

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


def buildARIMADataset():
    orders = Order.query.filter(Order.orderStatus.name == "FINISHED").all()
    dataset = defaultdict(list)

    for order in orders:
        waste_type_name = order.wasteType.name
        weight = order.weight
        orderDate = order.date

        dataset[waste_type_name].append([weight, orderDate])

    return dict(dataset)


def forecast_weight(dataset, days=7, order=(1, 1, 1)):  # 时间序列数据的自回归（AR）、差分（I）和移动平均（MA）部分
    # 考虑前一期的观察值（自回归阶数为1）、一阶差分（以使时间序列平稳）以及前一期的误差项（移动平均阶数为1）来预测当前值。
    forecasts = {}

    for category, data in dataset.items():
        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data, columns=['Weight', 'Date'])
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # 创建 ARIMA 模型并拟合
        model = ARIMA(df, order=order)
        fitted_model = model.fit()

        forecast = fitted_model.forecast(steps=days)

        forecasts[category] = forecast

    return forecasts


@government.route('/build_kmeans')
def build_kmeans():
    dataset = buildKmeansDataset()
    centers = TypeKmeansCenter(dataset)
    # Perform any additional processing or inference here
    return jsonify({'dataset': dataset, 'centers': centers})


@government.route('/build_arima')
def build_arima():
    dataset = buildARIMADataset()
    forecasts = forecast_weight(dataset)
    # Perform any additional processing or inference here
    return jsonify({'dataset': dataset, 'forecasts': forecasts})
