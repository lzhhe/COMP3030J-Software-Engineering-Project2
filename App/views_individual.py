from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

individual = Blueprint('individual', __name__, url_prefix='/individual')  # individual is name of blueprint


@individual.route('/index')
def index():
    return render_template('individual/index.html', methods=['POST'])

@individual.route('/createTemplate')
def createTemplate():
    user = g.user
    uid = user.UID

    data = request.get_json()
    wasteName = data.get('waste_name')
    wasteType = data.get('wasteType')
    attribution = data.get('attribution')

    new_template = UserTemplate(UID=uid, name=wasteName, wasteType=wasteType, attribution=attribution)
    db.session.add(new_template)
    db.session.commit()

    return jsonify({"message": f"This template has created"})

def parse_attributions(attr_str): # 解析json
    attr_dict = {}
    try:
        # 按空格拆分获取每个属性
        attributes = attr_str.split()
        for attribute in attributes:
            key, value = attribute.split(':')
            attr_dict[key] = value
    except Exception as e:
        print("Error parsing attributions:", e)
    return attr_dict

@individual.route('/getTemplate', methods=['GET'])
def getTemplate():
    user = g.user
    uid = user.UID
    try:
        templates = UserTemplate.query.filter_by(UID=uid).all()
        templates_data = [{
            'id': template.id,
            'name': template.name,
            'wasteType': template.wasteType.name,
            'attribution': parse_attributions(template.attribution)
        } for template in templates]

        return jsonify(templates_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 200

