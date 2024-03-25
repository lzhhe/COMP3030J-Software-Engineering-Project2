from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

department = Blueprint('department', __name__, url_prefix='/department')  # department is name of blueprint


@department.route('/')
@department.route('/main')
def main():
    return render_template('index.html')



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
        multiplier=data.get('multiplier', 1),  # 使用提供的值或默认为1
        comment=comment
    )

    # 添加到数据库并提交
    db.session.add(new_order)
    db.session.commit()

    # 返回成功消息
    return jsonify({"message": "Order created successfully"}), 201


