from datetime import datetime
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
    departmentType = None
    wastes = None
    user = g.user
    if user.department_id is not None:
        d = user.department
        department = d.departmentName
        departmentType = enum_to_string(d.departmentType)
        wasteTypes = Waste.query.filter_by(wasteDepartment=d.departmentType).all()
        wastes = {}
        for wasteType in wasteTypes:
            waste = enum_to_string(wasteType.wasteType)
            wastes[wasteType.wasteType.name] = waste
    return render_template('department/create_order.html', department=department, departmentType=departmentType,
                           wastes=wastes)


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
    weight = data.get('weight')
    attribution = data.get('attribution')
    comment = data.get('comment', '')  # 如果没有提供，使用空字符串
    # order_status = data.get('orderStatus', 'UNCONFIRMED')

    # 验证数据是否完整
    if not all([department_id, order_name, weight, attribution]):
        return jsonify({"error": "Missing required data for the order"}), 400

    # 创建新的工单记录
    new_order = Order(
        DID=department_id,
        date=datetime.utcnow(),
        orderName=order_name,
        weight=weight,
        attribution=attribution,
        comment=comment
    )

    # 添加到数据库并提交
    db.session.add(new_order)
    db.session.commit()

    # 返回成功消息
    return jsonify({"message": "Order created successfully"}), 201
