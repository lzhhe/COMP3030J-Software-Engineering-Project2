from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_, Date, func
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *
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


@waste.route('/approval')
def approval():
    # 状态统计
    status_counts = {
        'unconfirmed_count': Order.query.filter_by(orderStatus='UNCONFIRMED').count(),
        'confirmed_count': Order.query.filter_by(orderStatus='CONFIRM').count(),
        'processing_count': Order.query.filter_by(orderStatus='PROCESSING').count(),
        'finished_count': Order.query.filter_by(orderStatus='FINISHED').count()
    }
    queries = {}
    for i, status in enumerate(['UNCONFIRMED', 'CONFIRM', 'PROCESSING', 'FINISHED'], start=1):
        query = Order.query.filter_by(orderStatus=status)
        queries[f'orders{i}'] = query.all()
    all_departments = []
    for d in list(DepartmentType):
        all_departments.append(d)

    return render_template('waste/approval_order.html', **queries, **status_counts, all_departments=all_departments)


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
    # data = request.get_json()
    # OID = data.get('OID')
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
                return jsonify({"message": "successfully"}), 200
            else:
                return jsonify({
                    "message": f"The capacity of this type ({wasteType}) is overload if add this order into process"}), 200
    else:
        return jsonify({"error": "Order not found"}), 200


@waste.route('/finish/<OID>', methods=['POST'])
def finish(OID):
    # data = request.get_json()
    # OID = data.get('OID')
    if OID is None:
        return jsonify({"error": "Missing OID in request"}), 200
    order = Order.query.filter_by(OID=OID).first()
    if order:
        if order.orderStatus != OrderStatus.PROCESSING:
            return jsonify({"message": f"This order ({order.OID}) has not been in processing yet "})

        else:

            order.orderStatus = OrderStatus.FINISHED
            db.session.commit()
            return jsonify({"message": f"This order status ({order.OID}) has been changed to finish "})

    else:
        return jsonify({"error": "Order not found"}), 200


@waste.route('/modifyMultiplier/<OID>', methods=['PUT'])
def modifyMultiplier(OID):
    data = request.json
    print(OID)
    # OID = data.get('OID')
    newMultiplier = data.get('multiplier')
    print(newMultiplier)
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


@waste.route('/getRecentOrders', methods=['POST'])
def getRecentOrders():  # 需要一个天数作为参数，即多少天以前的，默认7天
    data = request.get_json()
    days_ago = data.get('date', 7)  # 获取多少天以前的
    department_id = data.get('department_id')
    past_date = datetime.now() - timedelta(days=days_ago)
    orders = Order.query.filter(Order.department_id == department_id, Order.date >= past_date).all()
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


@waste.route('/getOrdersStatus', methods=['POST'])  # 获取工单状态统计
def getOrdersStatus():
    data = request.get_json()
    department_id = data.get('department_id')

    order_counts = db.session.query(
        Order.orderStatus,
        func.count(Order.OID).label('count')
    ).filter_by(department_id=department_id
                ).group_by(Order.orderStatus).all()

    if order_counts:
        result = [
            {
                "orderStatus": status.name,
                "count": count
            }
            for status, count in order_counts
        ]
        return jsonify(result)
    else:
        return jsonify({"error": "No orders found for this department"}), 200


@waste.route('/getOrdersTypes', methods=['POST'])  # 获取工单状态统计
def getOrdersTypes():
    data = request.get_json()
    department_id = data.get('department_id')

    order_counts = db.session.query(
        Order.wasteType,
        func.count(Order.OID).label('count')
    ).filter_by(department_id=department_id
                ).group_by(Order.wasteType).all()

    if order_counts:
        result = [
            {
                "wasteType": wasteType.name,
                "count": count
            }
            for wasteType, count in order_counts
        ]
        return jsonify(result)
    else:
        return jsonify({"error": "No orders found for this department"}), 200


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
