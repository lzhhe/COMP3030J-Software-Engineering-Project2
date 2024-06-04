from collections import defaultdict, OrderedDict
from datetime import timedelta

import numpy as np
import pandas as pd
from pmdarima import auto_arima
from sklearn.cluster import KMeans

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
    start_time1 = time.time()
    dataset = buildKmeansDataset()
    start_time2 = time.time()
    centers = TypeKmeansCenter(dataset)
    start_time3 = time.time()
    centers = {category: center.tolist() for category, center in centers.items()}
    start_time4 = time.time()
    print("build dataset time", start_time2 - start_time1)
    print("kmeans calculation time", start_time3 - start_time2)
    print("index time", start_time4 - start_time3)
    print("total time", start_time4 - start_time1)
    print("KMeans Centers:", centers)
    return centers


@government.route('/forecast')
def forecast():
    wasteTypes = Waste.query.all()
    wastes = []
    for w in wasteTypes:
        wastes.append(w.wasteType)

    durationDataset = buildTimeDataset('HEAVY_METAL_WASTEWATER')
    d = {}
    for i, value in durationDataset.items():
        k = i.strftime('%Y-%m-%d')
        d[k] = sum(value) / len(value) if len(value) != 0 else 0
    durationForecasts = forecastTime(durationDataset)
    durationTrendDict = {}
    for i, value in enumerate(durationForecasts):
        forecast_date = (datetime.now().date() + timedelta(days=i+1)).strftime('%Y-%m-%d')
        forecast_date = str(forecast_date)
        durationTrendDict[forecast_date] = value

    weightDataset = buildWeightDataset('HEAVY_METAL_WASTEWATER')
    w = {}
    for i, value in weightDataset.items():
        k = i.strftime('%Y-%m-%d')
        w[k] = value
    weightForecasts = forecastWeight(weightDataset)

    weightTrendDict = {}
    for i, value in enumerate(weightForecasts):
        forecast_date = (datetime.now().date() + timedelta(days=i+1)).strftime('%Y-%m-%d')
        forecast_date = str(forecast_date)
        weightTrendDict[forecast_date] = value

    return render_template('government/forecast.html', wasteTypes=wastes,
                           durationDataset=d, durationTrend=durationTrendDict,
                           weightDataset=w,
                           weightTrend=weightTrendDict)


def generate_weight_dict():
    current_date = datetime.now().date()
    date_dict = {current_date - timedelta(days=i): 0.0 for i in range(30)}
    return date_dict


def buildWeightDataset(wasteType):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    orders = Order.query.filter(Order.orderStatus == "FINISHED", Order.wasteType == wasteType,
                                Order.date >= thirty_days_ago, Order.date < datetime.now()).all()

    dateDict = generate_weight_dict()

    for order in orders:
        multiplier = order.multiplier
        weight = float(order.weight * multiplier)
        order_date = order.date

        dateDict[order_date] = dateDict.get(order_date, 0) + weight

    sorted_dateDict = dict(sorted(dateDict.items(), key=lambda x: x[0]))
    return sorted_dateDict


def forecastWeight(dataset: dict, days=5):
    dates = [entry for entry in dataset.keys()]
    weights = [entry for entry in dataset.values()]
    df = pd.DataFrame({'Date': dates, 'Weight': weights})

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.asfreq('D')  # 强制频率为日

    model = auto_arima(df, seasonal=False, stepwise=True, suppress_warnings=True, error_action="ignore", trace=False)

    fitted_model = model.fit(df)
    forecast = fitted_model.predict(n_periods=days)

    return forecast.tolist()


@government.route('/getoneforecastweight/<wasteType>')
def get_one_forecast_weight(wasteType):
    weightDataset = buildWeightDataset(wasteType)
    w = {}
    for i, value in weightDataset.items():
        k = i.strftime('%Y-%m-%d')
        w[k] = value
    weightForecasts = forecastWeight(weightDataset)

    weightTrendDict = {}
    for i, value in enumerate(weightForecasts):
        forecast_date = (datetime.now().date() + timedelta(days=i+1)).strftime('%Y-%m-%d')
        forecast_date = str(forecast_date)
        weightTrendDict[forecast_date] = value
    print(w)

    return jsonify({'message': 'ok', 'weightDataset': w, 'weightTrend': weightTrendDict})


def generate_time_dict():
    current_date = datetime.now().date()
    date_values = {current_date - timedelta(days=i): [] for i in range(30)}
    return date_values


def buildTimeDataset(wasteType):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    orders = Order.query.filter(Order.orderStatus == "FINISHED", Order.wasteType == wasteType,
                                Order.date >= thirty_days_ago, Order.date < datetime.now() ).all()

    dateDict = generate_time_dict()

    for order in orders:
        order_date = order.date
        process_time = (order.finishDate - order.date).days

        if order_date not in dateDict:
            dateDict[order_date] = []
        dateDict[order_date].append(process_time)

    sorted_dateDict = dict(sorted(dateDict.items(), key=lambda x: x[0]))
    return sorted_dateDict


def forecastTime(dataset, days=5):
    dates = [entry for entry in dataset.keys()]
    times = [sum(entry) / len(entry) if len(entry) != 0 else 0 for entry in dataset.values()]
    # print(dates)
    # print(times)
    df = pd.DataFrame({'Date': dates, 'Times': times})

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.asfreq('D')  # 强制频率为日

    model = auto_arima(df, seasonal=False, stepwise=True, suppress_warnings=True, error_action="ignore", trace=False)

    fitted_model = model.fit(df)
    forecast = fitted_model.predict(n_periods=days)

    return forecast.tolist()


@government.route('/getoneforecastduration/<wasteType>')
def get_one_forecast_time(wasteType):
    durationDataset = buildTimeDataset(wasteType)
    d = {}
    for i, value in durationDataset.items():
        k = i.strftime('%Y-%m-%d')
        d[k] = sum(value) / len(value) if len(value) != 0 else 0
    durationForecasts = forecastTime(durationDataset)
    durationTrendDict = {}
    for i, value in enumerate(durationForecasts):
        forecast_date = (datetime.now().date() + timedelta(days=i+1)).strftime('%Y-%m-%d')
        forecast_date = str(forecast_date)
        durationTrendDict[forecast_date] = value

    return jsonify({'message': 'ok', 'durationDataset': d, 'durationTrend': durationTrendDict})


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
