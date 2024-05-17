import os
import time
from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash
from .views_utils import *

from .models import *

individual = Blueprint('individual', __name__, url_prefix='/individual')  # individual is name of blueprint


@individual.route('/index')
def index():
    return render_template('individual/index.html', methods=['POST'])


@individual.route('/create')
def create():
    api_key = "392c5833885dafa9515b33b18592414e"
    api_security = "2e288d9ae8003f33cc1b58b5fd941663"
    bing_api = "Alq9HEx7RGafIXHgY_oQiWYC9zxJWP-TTp5KZuGetS1YmaojcXw9FSa8cv_jeIKE"
    wastes = None
    user = g.user
    uid = user.UID
    if user is not None:
        wasteTypes = Waste.query.all()
        wastes = []
        for w in wasteTypes:
            wastes.append(w.wasteType)
    all_templates = getTemplates(uid)
    return render_template('individual/create.html', wastes=wastes, a1=api_security, a2=api_key, a3=bing_api,
                           all_templates=all_templates)


@individual.route('/createorder', methods=['POST'])
def createorder():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    user = g.user
    data = request.get_json()
    uid = user.UID
    order_name = data.get('orderName')
    waste_type = string_to_enum(data.get('wasteType'))
    weight = data.get('weight')
    attribution = data.get('attribution')
    address = data.get('address')
    comment = data.get('comment', '')

    # 验证数据是否完整
    if not all([order_name, weight, attribution, waste_type, address]):
        return jsonify({"message": "Missing required data for the order"}), 200

    # 创建新的工单记录
    new_order = Order(
        UID=uid,
        date=date.today(),
        wasteType=waste_type,
        orderName=order_name,
        weight=weight,
        attribution=attribution,
        comment=comment,
        address=address,
        wasteSource='EXTERNAL',
        orderStatus='UNCONFIRMED'
    )

    # 添加到数据库并提交
    db.session.add(new_order)
    db.session.commit()

    # 返回成功消息
    return jsonify({"message": "successful"}), 200


@individual.route('/contribution')
def contribution():
    global all_orders, orders_by_day
    user = g.user
    uid = user.UID
    if user is not None:
        all_orders = Order.query.filter_by(UID=uid).all()
        current_year = datetime.now().year
        orders_by_day = {}  # 用于存储每个日期的订单数量，格式为 {日期: 订单数量}
        for order in all_orders:
            order_date = order.date
            if order_date.year == current_year:
                date_str = order_date.strftime('%Y-%m-%d')
                orders_by_day[date_str] = orders_by_day.get(date_str, 0) + 1
    print(orders_by_day)

    return render_template('individual/contribution.html', all_orders=all_orders, orders_by_day=orders_by_day)


@individual.route('/recognize')
def recognize():
    user = g.user
    return render_template('individual/recognize.html')


@individual.route('/analyze-image', methods=['POST'])
def analyze_image():
    time.sleep(2)
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 200
        # 假设进行了某种形式的文件分析
    save_path = './analyze_store'
    file_path = os.path.join(save_path, file.filename)
    os.makedirs(save_path, exist_ok=True)
    file.save(file_path)
    analysis_result = perform_analysis(file)  # 这是伪代码
    print(file_path)
    os.remove(file_path)
    if analysis_result:
        return jsonify({'message': 'successful', 'data': analysis_result}), 200
    else:
        return jsonify({'message': 'analysis failed'}), 200


def perform_analysis(file):
    # 分析文件的逻辑
    return True  # 临时返回True，表示成功
