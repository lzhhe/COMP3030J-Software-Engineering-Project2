from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

login = Blueprint('login', __name__)  # department is name of blueprint


@login.route('/')
@login.route('/index')
def main():
    return render_template('login.html')

@login.route('/index')
def login(self):
    # 从请求中获取用户名和密码
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # 在数据库中查找用户
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # 密码验证成功
        session['UID'] = user.UID  # 使用Flask的session来保存用户状态
        return jsonify({'message': 'Login successful', 'user_id': user.UID}), 200
    else:
        # 用户名不存在或密码错误
        return jsonify({'message': 'Invalid username or password'}), 401




@login.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    status_str = data.get('status')

    if not all([username, password, email, status_str]):
        return jsonify({'message': 'Missing registration information'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409

    try:
        # 将状态字符串转换为枚举
        status = UserStatus[status_str]

        department_id = None
        if status == UserStatus.DEPARTMENT_MANAGER:
            department_name = data.get('departmentName')
            department = Department.query.filter_by(departmentName=department_name).first()
            if not department:
                return jsonify({'message': 'Invalid department name'}), 400
            department_id = department.DID

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            status=status,
            departmentID=department_id
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except KeyError:
        return jsonify({'message': 'Invalid user status'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

# 提供用户状态
@login.route('/user_statuses', methods=['GET'])
def get_user_statuses():
    statuses = [{"name": status.name, "value": status.value} for status in UserStatus]
    return jsonify(statuses)

# 给下拉菜单用
@login.route('/get_departments_name', methods=['GET'])
def get_departments_name():
    departments = Department.query.all()
    departments_list = []

    for department in departments:
        dept_info = {
            'departmentType': department.departmentType.name,
        }
        departments_list.append(dept_info)
    return jsonify(departments_list)
#获取所有部门信息
@login.route('/get_departments_info', methods=['GET'])
def get_departments_info():
    departments = Department.query.all()
    departments_list = []

    for department in departments:
        dept_info = {
            'DID': department.DID,
            'departmentName': department.departmentName,
            'departmentType': department.departmentType.name,
            'departmentAddress': department.departmentAddress,
            'managerId': department.managerId
        }
        departments_list.append(dept_info)

    return jsonify(departments_list)