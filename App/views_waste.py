from datetime import timedelta

from sklearn.tree import DecisionTreeRegressor

from .views_utils import *

waste = Blueprint('waste', __name__, url_prefix='/waste')  # waste is name of blueprint


@waste.route('/capacity')
def index():
    process_capacity = ProcessCapacity.query.all()
    waste_storage = WasteStorage.query.all()
    all_departments = []
    for d in list(DepartmentType):
        all_departments.append(d)
    return render_template('waste/capacity_dashboard.html', process_capacity=process_capacity,
                           waste_storage=waste_storage, all_departments=all_departments)


@waste.route('/approvalIN')
def approval1():
    all_internal_orders = Order.query.filter_by(wasteSource='INTERNAL').all()

    status_counts = {
        'unconfirmed_count': 0,
        'confirm_count': 0,
        'processing_count': 0,
        'finished_count': 0
    }
    orders1, orders2, orders3, orders4 = [], [], [], []
    orders_dict = {
        'UNCONFIRMED': orders1,
        'CONFIRM': orders2,
        'PROCESSING': orders3,
        'FINISHED': orders4
    }
    for order in all_internal_orders:
        if order.orderStatus.name in orders_dict:
            orders_dict[order.orderStatus.name].append(order)
            status_counts[f'{order.orderStatus.name.lower()}_count'] += 1
    queries = {
        'orders1': orders1,
        'orders2': orders2,
        'orders3': orders3,
        'orders4': orders4
    }
    all_departments = []
    for d in list(DepartmentType):
        all_departments.append(d)

    return render_template('waste/approval_order.html', **queries, **status_counts, all_departments=all_departments)


@waste.route('/approvalEX')
def approval2():
    # 状态统计
    all_uninternal_orders = Order.query.filter(Order.wasteSource != 'INTERNAL').all()

    status_counts = {
        'unconfirmed_count': 0,
        'confirm_count': 0,
        'processing_count': 0,
        'finished_count': 0
    }
    orders1, orders2, orders3, orders4 = [], [], [], []
    orders_dict = {
        'UNCONFIRMED': orders1,
        'CONFIRM': orders2,
        'PROCESSING': orders3,
        'FINISHED': orders4
    }
    for order in all_uninternal_orders:
        if order.orderStatus.name in orders_dict:
            orders_dict[order.orderStatus.name].append(order)
            status_counts[f'{order.orderStatus.name.lower()}_count'] += 1
    queries = {
        'orders1': orders1,
        'orders2': orders2,
        'orders3': orders3,
        'orders4': orders4
    }

    return render_template('waste/approval_order2.html', **queries, **status_counts)


@waste.route('/ratio')
def ratio():
    # 所有的订单
    allOrders = Order.query.all()
    unconfirmed_orders = Order.query.filter_by(orderStatus='UNCONFIRMED').all()
    confirmed_orders = Order.query.filter_by(orderStatus='CONFIRM').all()
    processing_orders = Order.query.filter_by(orderStatus='PROCESSING').all()
    finished_orders = Order.query.filter_by(orderStatus='FINISHED').all()
    nums = {
        'unconfirmed': len(unconfirmed_orders),
        'confirmed': len(confirmed_orders),
        'processing': len(processing_orders),
        'finished': len(finished_orders)
    }
    waste_weights = {enum_to_string(waste_type): 0 for waste_type in list(WasteType)}
    dept_orders = {enum_to_string(dept_type): 0 for dept_type in list(DepartmentType)}
    dept_weights = {enum_to_string(dept_type): 0 for dept_type in list(DepartmentType)}
    for order in allOrders:
        if enum_to_string(order.wasteType) in waste_weights:
            waste_weights[enum_to_string(order.wasteType)] += order.weight
        if enum_to_string(order.department.departmentType) in dept_orders:
            dept_orders[enum_to_string(order.department.departmentType)] += 1
            dept_weights[enum_to_string(order.department.departmentType)] += order.weight
    all_departments = []
    for d in list(DepartmentType):
        all_departments.append(d)

    return render_template('waste/ratio_order.html', nums=nums, waste_weights=waste_weights,
                           dept_weights=dept_weights, dept_orders=dept_orders, all_departments=all_departments)


# 工单处理相关
@waste.route('/confirm/<OID>', methods=['PUT'])
def confirm(OID):
    # data = request.get_json()
    # OID = data.get('OID')
    if OID is None:
        return jsonify({"error": "Missing OID in request"}), 200
    order = Order.query.filter_by(OID=OID).first()
    if order:
        # 检查储存库占用
        wasteType = order.wasteType
        weight = order.weight
        wasteStorage = WasteStorage.query.filter_by(wasteType=wasteType).first()
        maxCapacity = wasteStorage.maxCapacity
        currentCapacity = wasteStorage.currentCapacity
        if currentCapacity + weight <= maxCapacity:
            # 能力之内才能储存
            order.orderStatus = OrderStatus.CONFIRM
            wasteStorage.currentCapacity = wasteStorage.currentCapacity + weight
            db.session.commit()
            return jsonify({"message": "Order confirmed successfully"}), 200
        else:
            return jsonify(
                {"message": f"The Storage of is {enum_to_string(wasteType)} overload if add this order"}), 200

    else:
        return jsonify({"err": "Order not found"}), 200


@waste.route('/process/<OID>', methods=['PUT'])
def process(OID):
    if OID is None:
        return jsonify({"error": "Missing OID in request"}), 200
    order = Order.query.filter_by(OID=OID).first()
    if order:
        if order.orderStatus != OrderStatus.CONFIRM:
            return jsonify({"message": f"This order ({order.OID})has not confirmed yet "})

        else:
            multiplier = order.multiplier
            wasteType = order.wasteType
            weight = order.weight
            processCapacity = ProcessCapacity.query.filter_by(wasteType=wasteType).first()

            maxCapacity = processCapacity.maxCapacity
            currentCapacity = processCapacity.currentCapacity

            if currentCapacity + weight * multiplier <= maxCapacity:  # 增加处理能力占用倍率
                order.orderStatus = OrderStatus.PROCESSING
                processCapacity.currentCapacity = processCapacity.currentCapacity + weight * multiplier
                wasteStorage = WasteStorage.query.filter_by(wasteType=wasteType).first()
                wasteStorage.currentCapacity = wasteStorage.currentCapacity - weight
                db.session.commit()

                forecastTime = predict_weight(wasteType, weight)
                forecastFinishDate = order.date + timedelta(days=forecastTime)
                # print(forecastFinishDate)
                order.finishDate = forecastFinishDate
                db.session.commit()

                return jsonify({"message": "successfully", "fdate": forecastFinishDate}), 200
            else:
                return jsonify({
                    "message": f"The capacity of this type ({wasteType}) is overload if add this order into process"}), 200

    else:
        return jsonify({"error": "Order not found"}), 200


@waste.route('/finish/<OID>', methods=['PUT'])
def finish(OID):
    # data = request.get_json()
    # OID = data.get('OID')
    if OID is None:
        return jsonify({"error": "Missing OID in request"}), 200
    order = Order.query.filter_by(OID=OID).first()
    if order:
        if order.orderStatus != OrderStatus.PROCESSING:
            return jsonify({"message": f"This order ({order.OID}) has not been in processing yet "}), 200
        else:
            order.orderStatus = OrderStatus.FINISHED
            order.finishDate = datetime.today()  # 记录完成时间
            db.session.commit()

            # 恢复处理仓的能力
            processCapacity = ProcessCapacity.query.filter_by(wasteType=order.wasteType).first()
            processCapacity.currentCapacity = processCapacity.currentCapacity - order.weight * order.multiplier
            db.session.commit()
            return jsonify({"message": "successfully"}), 200
    else:
        return jsonify({"error": "Order not found"}), 200


@waste.route('/modifyMultiplier/<OID>', methods=['PUT'])
def modifyMultiplier(OID):
    data = request.json
    # print(OID)
    # OID = data.get('OID')
    newMultiplier = data.get('multiplier')
    # print(newMultiplier)
    order = Order.query.filter_by(OID=OID).first()
    order.multiplier = newMultiplier
    db.session.commit()
    return jsonify(), 200


# 工单相关
@waste.route('/getAllOrders', methods=['POST'])
def getAllOrders():
    data = request.get_json()
    department_id = data.get('department_id')
    orders = Order.query.filter_by(department_id=department_id)
    if orders:
        order_list = []
        for order in orders:
            order_data = {
                'OID': order.OID,
                'date': order.date.isoformat(),
                'orderName': order.orderName,
                'wasteType': order.wasteType.name,
                'weight': order.weight,
                'attribution': order.attribution,
                'multiplier': order.multiplier,
                'comment': order.comment,
                'orderStatus': order.orderStatus.name,
                'DID': order.department.DID,
                'departmentName': order.department.departmentName
            }
            order_list.append(order_data)
        return jsonify(order_list)
    else:
        return jsonify({"error": "You have not summit any order"}), 200


# 处理相关
@waste.route('/getStorage', methods=['POST'])  # 获取库存状态
def getStorage():
    storages = WasteStorage.query.all()

    result = [
        {
            "wasteType": storage.wasteType.name,
            "maxCapacity": storage.maxCapacity,
            "currentCapacity": storage.currentCapacity,
            "occupancyRate": storage.currentCapacity / storage.maxCapacity  # 使用占比，可以做一个切换
        }
        for storage in storages
    ]

    return jsonify(result)


@waste.route('/getProcess', methods=['POST'])  # 获取处理舱存状态
def getProcess():
    Processes = WasteStorage.query.all()

    result = [
        {
            "wasteType": Process.wasteType.name,
            "maxCapacity": Process.maxCapacity,
            "currentCapacity": Process.currentCapacity,
            "occupancyRate": Process.currentCapacity / Processes.maxCapacity
        }
        for Process in Processes
    ]

    return jsonify(result)


def buildTimeDataset(wasteType):
    # 获取最近30天内的订单数据
    thirty_days_ago = datetime.now() - timedelta(days=30)
    orders = Order.query.filter(Order.orderStatus == "FINISHED", Order.wasteType == wasteType,
                                Order.date >= thirty_days_ago).all()
    X_train = []
    Y_train = []
    temp_train = []
    # 构建每个类别的时间序列
    for order in orders:
        process_time = (order.finishDate - order.date).days  # 计算处理时间（天）
        order_weight = order.weight
        X_train.append([order_weight])
        Y_train.append(process_time)
    # print(X_train, Y_train)
    return X_train, Y_train


def build_decisionTree(X_train, y_train, weight):
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)

    weight_2d = [[weight]]

    predicted_time = model.predict(weight_2d)

    return int(predicted_time)


def predict_weight(wasteType, weight):
    X_train, Y_train = buildTimeDataset(wasteType)
    predict_time = build_decisionTree(X_train, Y_train, weight)
    # print("predict: ", predict_time)
    return predict_time
