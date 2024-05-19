from copy import deepcopy
from collections import defaultdict
from copy import deepcopy
from datetime import timedelta

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA

from .models import *
from .views_utils import *

government = Blueprint('government', __name__, url_prefix='/government')  # government is name of blueprint


@government.route('/index')
def index():
    return render_template('government/index.html')


@government.route('/freeproportion')
def free_p():
    free_query = FreeProportion.query.all()
    return render_template('government/free_proportion.html', free_list=free_query)


@government.route('statistics')
def statistics():
    today = datetime.now()
    last_year_today = today - timedelta(days=365)
    orders = Order.query.filter(Order.date.between(last_year_today, today)).all()
    daily_weight = {}
    for order in orders:
        daily_weight[order.date] = daily_weight.get(order.date, 0) + order.weight
    sorted_daily_weight = {k: daily_weight[k] for k in sorted(daily_weight)}

    centerForecast = build_kmeans()
    scatter_data = []
    categories = list(centerForecast.keys())  # 保留垃圾类型的列表
    categories_string = []
    for ca in categories:
        categories_string.append(ca.replace('_', ' ').title())
    for idx, category in enumerate(categories):
        center = centerForecast[category][0]
        scatter_data.append([idx, center[0], center[1]])  # X, Y, Z
    return render_template('government/statistics.html', daily_weight=sorted_daily_weight,
                           scatter_data=scatter_data, categories_string=categories_string)


@government.route('/forecast')
def forecast():
    wasteTypes = Waste.query.all()
    wastes = []
    for w in wasteTypes:
        wastes.append(w.wasteType)
    return render_template('government/forecast.html', wasteTypes=wastes)


def buildKmeansDataset():
    orders = Order.query.filter(Order.orderStatus == "FINISHED").all()
    dataset = defaultdict(list)

    for order in orders:
        waste_type_name = order.wasteType.name
        weight = order.weight
        duration = (order.finishDate - order.date).days

        dataset[waste_type_name].append((weight, duration))

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
    return centers


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
            dataset[waste_type_name] = deepcopy(dateList)  # 深拷贝 dateList

        for entry in dataset[waste_type_name]:
            if entry[0] == order_date:
                entry[1] = entry[1] + weight
                break

    # 对每个类别的数据按日期进行排序
    for category in dataset:
        dataset[category].sort(key=lambda x: x[0])

    print("weight dataset: ", dict(dataset))
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
    dateList = generate_time_array()  # [date, []]

    # 构建每个类别的时间序列
    for order in orders:
        waste_type_name = order.wasteType.name
        order_date = order.date
        process_time = (order.finishDate - order.date).days  # 计算处理时间（天）

        # 检查废物类型是否在数据集中，如果不在，则初始化为 dateList
        if waste_type_name not in dataset:
            dataset[waste_type_name] = deepcopy(dateList)  # 深拷贝 dateList

        # print("category: ", waste_type_name)
        for entry in dataset[waste_type_name]:
            if entry[0] == order_date:
                # print("category: ", waste_type_name, " date: ", order_date, " process time: ", process_time)
                entry[1].append(process_time)
                # print(entry)
                break

    for category in dataset:
        dataset[category].sort(key=lambda x: x[0])
    print("Time dataset: ", dict(dataset))
    return dict(dataset)


def forecastTime(dataset, days=5, order=(1, 1, 1)):
    forecasts = {}
    for category, data in dataset.items():
        # 提取每个类别的重量和日期数据
        dates = [entry[0] for entry in data]
        # print(dates)
        times = []
        for entry in data:
            if len(entry[1]) != 0:
                averageTime = sum(entry[1]) / len(entry[1])
            else:
                averageTime = 0
            times.append(averageTime)
        # print(times)
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
    print("Weight Forecasts:", weightForecasts)

    timeDataset = buildTimeDataset()
    timeForecasts = forecastTime(timeDataset)
    timeForecasts = {category: forecast for category, forecast in timeForecasts.items()}
    print("Time Forecasts:", timeForecasts)
    return jsonify({'weight_forecasts': weightForecasts, 'time_forecasts': timeForecasts})
    # return jsonify({'forecasts': weightForecasts})


'''更改免费份额'''


@government.route('/adjust_free_proportion', methods=['POST'])
def adjust_free_proportion():
    data = request.json
    freeList = data.get('freeList')
    if not freeList:
        return jsonify({"error": "Invalid request, freeList is missing"}), 200
    for item in freeList:
        wasteType = item.get('wasteType')
        newProportion = int(item.get('freeProportion'))
        # 查询当前的废物比例
        freeProportionLine = FreeProportion.query.filter_by(wasteType=wasteType).first()
        if not freeProportionLine:
            continue  # 如果没有找到对应的废物类型，则跳过
        oldProportion = freeProportionLine.freeProportion
        # 更新比例
        freeProportionLine.freeProportion = newProportion
        # 计算比例差异
        differenceProportion = newProportion - oldProportion
        # 查询处理能力
        max_capacity = ProcessCapacity.query.filter_by(wasteType=wasteType).first()
        if max_capacity:
            freeProportionLine.freeCapacity = freeProportionLine.freeCapacity + 0.01 * (
                    max_capacity.maxCapacity * differenceProportion)
        db.session.commit()
    return jsonify({"message": "successful"}), 200


@government.route('/update_free_proportion')
def update_free_proportion_monthly():
    current_date = datetime.now()
    if current_date.day == 1:
        renew_free_capacity()


def renew_free_capacity():
    free_proportions = FreeProportion.query.all()

    for free_proportion in free_proportions:
        max_capacity = ProcessCapacity.query.filter_by(wasteType=free_proportion.wasteType).first().maxCapacity
        new_free_capacity = max_capacity * free_proportion.freeProportion
        free_proportion.freeCapacity = new_free_capacity
    db.session.commit()
