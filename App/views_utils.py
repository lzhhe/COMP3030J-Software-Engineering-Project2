import time
from datetime import datetime
from functools import wraps
from zhipuai import ZhipuAI
from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify, Response
from flask_babel import refresh
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

utils = Blueprint('utils', __name__)  # department is name of blueprint

my_client = ZhipuAI(api_key='3f093e7f95656722be8262fdf323db43.PuQs4UvOcDHwDcDt')
waste_types_info_zh = """
在我们的网站上，您可以找到多种废弃物类型供您选择。选择一种废弃物类型来创建订单，我们将帮助您处理这些废弃物，让地球变得更加绿色。我们处理的废弃物包括：
- **冶金类废物**
  - 重金属废水 (HEAVY_METAL_WASTEWATER)
  - 废气 (EXHAUST_GAS)
  - 矿物残渣 (MINERAL_RESIDUE)
- **高端机械设备制造类废物**
  - 切削液 (CUTTING_FLUID)
  - 金属屑 (METAL_CHIPS)
  - 塑料 (PLASTIC)
  - 复合材料切割废料 (COMPOSITE_MATERIAL_CUTTING_WASTE)
  - 废漆 (WASTE_PAINT)
- **复合材料制造类废物**
  - 粉尘 (DUST)
  - 化学品 (CHEMICALS)
  - 催化剂 (CATALYZER)
- **新能源类废物**
  - 化学推进剂 (CHEMICAL_PROPELLANTS)
  - 燃料残渣 (FUEL_RESIDUES)
- **自动化系统类废物**
  - 废弃电子元器件 (DISCARDED_ELECTRONIC_COMPONENTS)
- **设备维护类废物**
  - 液压油 (HYDRAULIC_OIL)
  - 润滑油废料 (LUBRICANT_WASTE)
- **实验室类废物**
  - 有害化学品 (HAZARDOUS_CHEMICALS)
  - 废弃实验器材 (WASTE_EXPERIMENTAL_EQUIPMENT)
- **数据中心类废物**
  - 废热 (WASTE_HEAT)
- **行政类废物**
  - 废纸 (WASTE_PAPER)
  - 生活垃圾 (HOUSEHOLD_WASTE)
  
**订单流程：**
1. 创建订单后，订单将首先处于未确认状态。
2. 废物管理员将审核并确认您的订单。
3. 确认后，废弃物将被添加到废物储存仓库中。
4. 仓库中的废弃物将被同意进行处理，我们的系统拥有处理能力。
5. 如果订单需要大量的处理能力，甚至超过处理能力，则不会进行处理。
6. 对于每个订单，需要选择相应废弃物的类型和重量，以及一些特殊属性，例如二氧化碳含量等。
7. 订单确认后，系统将对其进行智能判断，以确定是否需要更多的处理能力。

作为用户，您可以看到公司对环境的优化工作。让我们一起努力，为了地球的绿色未来！
"""

waste_types_info_en = """
On our website, you can find a variety of waste types for you to choose from. Select a waste type to create an order, and we will help you dispose of these wastes, making the Earth greener. The types of waste we handle include:

- **Metallurgical Waste**
  - Heavy Metal Wastewater (HEAVY_METAL_WASTEWATER)
  - Exhaust Gas (EXHAUST_GAS)
  - Mineral Residue (MINERAL_RESIDUE)
- **High-End Machinery Manufacturing Waste**
  - Cutting Fluid (CUTTING_FLUID)
  - Metal Chips (METAL_CHIPS)
  - Plastic (PLASTIC)
  - Composite Material Cutting Waste (COMPOSITE_MATERIAL_CUTTING_WASTE)
  - Waste Paint (WASTE_PAINT)
- **Composite Material Manufacturing Waste**
  - Dust (DUST)
  - Chemicals (CHEMICALS)
  - Catalyst (CATALYZER)
- **New Energy Waste**
  - Chemical Propellants (CHEMICAL_PROPELLANTS)
  - Fuel Residues (FUEL_RESIDUES)
- **Automation System Waste**
  - Discarded Electronic Components (DISCARDED_ELECTRONIC_COMPONENTS)
- **Equipment Maintenance Waste**
  - Hydraulic Oil (HYDRAULIC_OIL)
  - Lubricant Waste (LUBRICANT_WASTE)
- **Laboratory Waste**
  - Hazardous Chemicals (HAZARDOUS_CHEMICALS)
  - Waste Experimental Equipment (WASTE_EXPERIMENTAL_EQUIPMENT)
- **Data Center Waste**
  - Waste Heat (WASTE_HEAT)
- **Administrative Waste**
  - Waste Paper (WASTE_PAPER)
  - Household Waste (HOUSEHOLD_WASTE)
**Order Process:**
1. After creating an order, it will first be in an unconfirmed status.
2. A waste manager will review and confirm your order.
3. Once confirmed, the waste will be added to the waste storage warehouse.
4. The waste in the warehouse will be approved for processing, and our system has processing capacity.
5. If the order requires a significant amount of processing capacity, or even more than the processing capacity, it will not be processed.
6. For each order, you need to select the type and weight of the corresponding waste, as well as some special attributes, such as carbon dioxide content, etc.
7. After the order is confirmed, the system will make an intelligent judgment on it to determine if more processing capacity is needed.

As a user, you can see the company's optimization of the environment. Let's work together for a greener future for the Earth!
"""


def generate_stream(ai_response):
    try:
        for chunk in ai_response:
            # Simulating a delay for each message chunk
            yield f"{chunk.choices[0].delta.content}"
    except GeneratorExit:
        print("Client disconnected")


@utils.route('/api/ai-assistant', methods=['GET', 'POST'])
def ai_assistant():
    if request.method == 'GET':
        return jsonify({'success': True, 'message': 'AI assistant is running'})
    else:
        data = request.get_json()
        user_message = data.get('message')
        # 使用智谱AI的API进行消息处理
        ai_response = my_client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": waste_types_info_en},
                {"role": "user", "content": user_message}
            ],
            stream=True,
        )
        return Response(generate_stream(ai_response), content_type='text/event-stream')


@utils.route('/switch_theme', methods=['POST'])
def switchTheme():
    theme = request.form.get('theme')
    session['theme'] = theme
    return jsonify({'success': True, 'message': 'Theme switched successfully'})


@utils.route('/switch_language', methods=['POST'])
def switchLanguage():
    language = request.form.get('language')
    session['language'] = language
    refresh()
    return jsonify({'success': True, 'message': 'Language switched successfully'})


def enum_to_string(enum):
    return enum.name.replace('_', ' ').title()


def string_to_enum(string):
    return string.replace(' ', '_').upper()

@utils.route('/createTemplate')
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

@utils.route('/getTemplate', methods=['GET'])
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

