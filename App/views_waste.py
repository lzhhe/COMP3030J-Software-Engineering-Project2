from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_, Date
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

waste = Blueprint('waste', __name__, url_prefix='/waste')  # waste is name of blueprint


@waste.route('/')
def index():
    return render_template('waste/index.html')


@waste.route('/orderList', methods=['POST'])
def orderList():
    user = g.user
    orders = Order.query.filter_by(UID=user.UID).all()

    # Prepare the data for JSON conversion
    order_list = []
    for order in orders:
        order_data = {
            'OID': order.OID,
            'date': order.date.isoformat(),  # Convert date to ISO format string
            'orderName': order.orderName,
            'wasteType': order.wasteType.name,  # Assuming you want the name of the Enum
            'weight': order.weight,
            'attribution': order.attribution,
            'multiplier': order.multiplier,
            'comment': order.comment,
            'orderStatus': order.orderStatus.name  # Assuming you want the name of the Enum
        }
        # Add department data if present
        if order.department:
            order_data['department'] = {
                'DID': order.department.DID,
                'departmentName': order.department.departmentName
            }
        order_list.append(order_data)

    # Return the list of orders in JSON format
    return jsonify(order_list)


@waste.route('/confirm', methods=['POST'])
def confirm():
    data = request.get_json()
    OID = data.get('OID')
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
            db.session.commit()
            return jsonify({"message": "Order confirmed successfully"}), 200
        else:
            return jsonify({"message": f"The Storage of is {wasteType} overload if add this order"}), 200

    else:
        return jsonify({"error": "Order not found"}), 200


@waste.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    OID = data.get('OID')
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
                db.session.commit()
                return jsonify({"message": "Order will be in process"}), 200
            else:
                return jsonify({
                    "message": f"The capacity of this type ({wasteType}) is overload if add this order into process"}), 200
    else:
        return jsonify({"error": "Order not found"}), 200


@waste.route('/finish', methods=['POST'])
def finish():
    data = request.get_json()
    OID = data.get('OID')
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


@waste.route('/modifyMultiplier', methods=['POST'])
def modifyMultiplier():
    data = request.get_json()
    OID = data.get('OID')
    newMultiplier = data.get('multiplier')
    order = Order.query.filter_by(OID=OID).first()
    order.multiplier = newMultiplier
    db.session.commit()


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
def getRecentOrders(): # 需要一个天数作为参数，即多少天以前的，默认7天
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



