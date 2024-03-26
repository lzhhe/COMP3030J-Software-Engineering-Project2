from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

waste = Blueprint('waste', __name__, template_folder='templates')  # waste is name of blueprint


@waste.route('/')
def index():
    return render_template('waste/index.html')


@waste.route('/confirm', methods=['POST'])
def confirm():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.get_json()
    OID = data.get('OID')
    if OID is None:
        return jsonify({"error": "Missing OID in request"}), 400
    order = Order.query.filter_by(OID=OID).first()
    if order:
        # 更新工单状态为CONFIRM
        order.orderStatus = OrderStatus.CONFIRM
        db.session.commit()
        return jsonify({"message": "Order confirmed successfully"}), 200
    else:
        return jsonify({"error": "Order not found"}), 404
