from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *
from .views_utils import enum_to_string, string_to_enum

department = Blueprint('department', __name__, url_prefix='/department')  # department is name of blueprint


@department.route('/')
def index():
    department = None
    departmentDID = 0
    departmentType = None
    wastes = None
    user = g.user
    if user.department_id is not None:
        d = user.department
        department = d.departmentName
        departmentDID = d.DID
        departmentType = enum_to_string(d.departmentType)
        wasteTypes = Waste.query.filter_by(wasteDepartment=d.departmentType).all()
        wastes = {}
        for wasteType in wasteTypes:
            waste = enum_to_string(wasteType.wasteType)
            wastes[wasteType.wasteType.name] = waste
    return render_template('department/create_order.html', department=department, departmentType=departmentType,
                           wastes=wastes, departmentDID=departmentDID)


@department.route('/setdepartment', methods=['POST'])
def setdepartment():
    user = g.user
    data = request.json
    departmentType = data.get('departmentType')
    departmentName = data.get('departmentName')
    departmentAddress = data.get('departmentAddress')
    if Department.query.filter_by(departmentName=departmentName).first():
        return jsonify({"message": "Department name already exists"}), 200
    try:
        new_department = Department(departmentName=departmentName, departmentType=departmentType,
                                    departmentAddress=departmentAddress)
        db.session.add(new_department)
        db.session.commit()
        user.department_id = new_department.DID
        db.session.commit()
        return jsonify({"message": "successful"}), 200
    except KeyError:
        return jsonify({'message': 'Invalid user status'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 200


@department.route('/edit')
def edit():
    return render_template('department/edit_order.html')


@department.route('/history')
def history():
    return render_template('department/view_order.html')


@department.route('/dashboard')
def dashboard():
    return render_template('department/dashboard.html')


@department.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    department_id = data.get('departmentID')
    order_name = data.get('orderName')
    waste_type = data.get('wasteType')
    weight = data.get('weight')
    attribution = data.get('attribution')
    comment = data.get('comment', '')  # 如果没有提供，使用空字符串
    # order_status = data.get('orderStatus', 'UNCONFIRMED')

    # 验证数据是否完整
    if not all([department_id, order_name, weight, attribution, waste_type]):
        return jsonify({"message": "Missing required data for the order"}), 200

    # 创建新的工单记录
    new_order = Order(
        department_id=department_id,
        date=date.today(),
        wasteType=waste_type,
        orderName=order_name,
        weight=weight,
        attribution=attribution,
        comment=comment,
        orderStatus='UNCONFIRMED'
    )

    # 添加到数据库并提交
    db.session.add(new_order)
    db.session.commit()

    # 返回成功消息
    return jsonify({"message": "successful"}), 200


@department.route('/getAllOrders', methods=['POST'])
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


@department.route('/getRecentOrders', methods=['POST'])
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
