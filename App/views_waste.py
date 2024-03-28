from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
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

            wasteType = order.wasteType
            weight = order.weight

            processCapacity = ProcessCapacity.query.filter_by(wasteType=wasteType).first()

            maxCapacity = processCapacity.maxCapacity
            currentCapacity = processCapacity.currentCapacity

            if currentCapacity + weight <= maxCapacity:
                order.orderStatus = OrderStatus.CONFIRM
                db.session.commit()
                return jsonify({"message": "Order will be in process"}), 200
            else:
                return jsonify({
                                   "message": f"The capacity of this type ({wasteType}) is overload if add this order into process"}), 200
    else:
        return jsonify({"error": "Order not found"}), 200
