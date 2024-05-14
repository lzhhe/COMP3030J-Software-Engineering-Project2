from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from flask_babel import Babel, gettext as _
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

login = Blueprint('login', __name__)  # department is name of blueprint


@login.route('/')
def main():
    return render_template('base2.html')


@login.route('/lpage')
def lpage():
    return render_template('login.html')


@login.route('/login', methods=['POST'])
def log():
    # 从请求中获取用户名和密码
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 200

    # 在数据库中查找用户
    user = User.query.filter_by(username=username).first()

    # if user and check_password_hash(user.password, password):
    if user and user.password == password:
        # 密码验证成功
        # if user.status.name == 'WASTE_MANAGER':
        #     should_finished_orders = Order.query.filter_by(orderStatus='PROCESSING').all()
        #     for order in should_finished_orders:
        #         if order.finishDate < datetime.today().date():
        #             order.orderStatus = OrderStatus.FINISHED
        #             order.finishDate = datetime.today()
        #     db.session.commit()
        session['UID'] = user.UID  # 使用Flask的session来保存用户状态
        return jsonify({'message': 'Login successful', 'status': user.status.name}), 200
    else:
        # 用户名不存在或密码错误
        return jsonify({'message': 'Invalid username or password'}), 200


@login.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    status = data.get('status')

    if not all([username, password, email, status]):
        return jsonify({'message': 'Missing registration information'}), 200

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 200

    try:

        new_user = User(
            username=username,
            password=password,
            email=email,
            status=status,
        )

        db.session.add(new_user)
        db.session.commit()
        session['UID'] = new_user.UID  # 使用Flask的session来保存用户状态

        return jsonify({'message': 'successful', 'status': status}), 200
    except KeyError:
        return jsonify({'message': 'Invalid user status'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 200


@login.route('/forget', methods=['POST'])
def forget():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print(username, password, email)

    if not username or not password or not email:
        return jsonify({'message': 'Missing registration information'}), 200
    else:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Invalid username'}), 200
        elif user and email != user.email:
            return jsonify({'message': 'Invalid email'}), 200
        else:
            user.password = password
            db.session.commit()
            session['UID'] = user.UID  # 使用Flask的session来保存用户状态
            return jsonify({'message': 'successful', 'status': user.status.name}), 200


@login.route('/logout', methods=['GET'])
def logout():
    session.pop('UID', None)
    return redirect(url_for('login.main'))


# # 提供用户状态
@login.route('/user_statuses', methods=['GET'])
def get_user_statuses():
    statuses = [{"name": status.name, "value": status.value} for status in UserStatus]
    return jsonify(statuses)


#
#
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


#
#
# 获取所有部门信息
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
