import base64
import io
import random
import re
import string

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

from .views_utils import *

individual = Blueprint('individual', __name__, url_prefix='/individual')  # individual is name of blueprint


@individual.route('/index')
def index():
    return render_template('individual/index.html', methods=['POST'])


@individual.route('/create')
def create():
    api_key = "392c5833885dafa9515b33b18592414e"
    api_security = "2e288d9ae8003f33cc1b58b5fd941663"
    bing_api = "AhW0o1eP-z1W5DblVYgvO5Pp10Mh3YBqhw97xKJCMJNXJXr027Z7IQMPibvr09aA"
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


def generate_verification_code(length=6):
    # 生成指定长度的随机字母数字组合
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@individual.route('/check_free_proportion', methods=['POST'])
def check_free_proportion():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.get_json()
    waste_type = string_to_enum(data.get('wasteType'))
    weight = int(data.get('weight'))
    if use_free_proportion(waste_type, weight):
        return jsonify({"status": "OK"}), 200
    else:
        # 超出免费份额，生成验证码
        code = generate_verification_code()
        return jsonify({"status": "OVER_LIMIT", "code": code}), 200


@individual.route('/createorder', methods=['POST'])
def createorder():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    user = g.user
    data = request.get_json()
    uid = user.UID
    order_name = data.get('orderName')
    waste_type = string_to_enum(data.get('wasteType'))
    weight = int(data.get('weight'))
    attribution = data.get('attribution')
    address = data.get('address')
    comment = data.get('comment', '')

    free = data.get('free')

    # 验证数据是否完整
    if not all([order_name, weight, attribution, waste_type, address]):
        return jsonify({"message": "Missing required data for the order"}), 200

    # 创建新的工单记录
    if free:
        wasteSource = "EXTERNAL_FREE"
        free_proportion = FreeProportion.query.filter_by(wasteType=waste_type).first()
        available_capacity = free_proportion.freeCapacity
        free_proportion.freeCapacity = available_capacity - weight
        db.session.commit()
    else:
        wasteSource = "EXTERNAL"

    new_order = Order(
        UID=uid,
        date=date.today(),
        wasteType=waste_type,
        orderName=order_name,
        weight=weight,
        attribution=attribution,
        comment=comment,
        address=address,
        wasteSource=wasteSource,
        orderStatus='UNCONFIRMED'
    )

    # 添加到数据库并提交
    db.session.add(new_order)
    db.session.commit()

    # 返回成功消息
    return jsonify({"message": "successful"}), 200


def use_free_proportion(wasteType, weight):
    free_proportion = FreeProportion.query.filter_by(wasteType=wasteType).first()
    available_capacity = free_proportion.freeCapacity
    if available_capacity - weight >= 0:
        return True
    else:
        return False


waste_contribution = {
    WasteType.HEAVY_METAL_WASTEWATER: {'tree': 0.001, 'water': 0.5, 'air': 0, 'soil': 0.01, 'energy': 0},
    WasteType.EXHAUST_GAS: {'tree': 0.01, 'water': 0, 'air': 1, 'soil': 0.0005, 'energy': 0.1},
    WasteType.MINERAL_RESIDUE: {'tree': 0.002, 'water': 0.2, 'air': 0.1, 'soil': 0.02, 'energy': 0.2},
    WasteType.CUTTING_FLUID: {'tree': 0.003, 'water': 1, 'air': 0.4, 'soil': 0.04, 'energy': 0.3},
    WasteType.METAL_CHIPS: {'tree': 0.003, 'water': 0.6, 'air': 0.3, 'soil': 0.03, 'energy': 0.2},
    WasteType.PLASTIC: {'tree': 0.002, 'water': 0.4, 'air': 0.1, 'soil': 0.02, 'energy': 0.15},
    WasteType.COMPOSITE_MATERIAL_CUTTING_WASTE: {'tree': 0.003, 'water': 1, 'air': 0.4, 'soil': 0.04, 'energy': 0.3},
    WasteType.WASTE_PAINT: {'tree': 0.002, 'water': 0.5, 'air': 0.3, 'soil': 0.01, 'energy': 0.1},
    WasteType.DUST: {'tree': 0.01, 'water': 0.02, 'air': 1, 'soil': 0.0005, 'energy': 0.05},
    WasteType.CHEMICALS: {'tree': 0.004, 'water': 1, 'air': 0.4, 'soil': 0.04, 'energy': 0.3},
    WasteType.CATALYZER: {'tree': 0.005, 'water': 0.8, 'air': 0.3, 'soil': 0.04, 'energy': 0.5},
    WasteType.CHEMICAL_PROPELLANTS: {'tree': 0.005, 'water': 0.8, 'air': 0.3, 'soil': 0.04, 'energy': 0.5},
    WasteType.FUEL_RESIDUES: {'tree': 0.002, 'water': 0.8, 'air': 0.1, 'soil': 0.02, 'energy': 0.8},
    WasteType.DISCARDED_ELECTRONIC_COMPONENTS: {'tree': 0.004, 'water': 0.5, 'air': 0.3, 'soil': 0.1, 'energy': 0.2},
    WasteType.HYDRAULIC_OIL: {'tree': 0.004, 'water': 1, 'air': 0.4, 'soil': 0.04, 'energy': 0.3},
    WasteType.LUBRICANT_WASTE: {'tree': 0.004, 'water': 1, 'air': 0.4, 'soil': 0.04, 'energy': 0.3},
    WasteType.HAZARDOUS_CHEMICALS: {'tree': 0.005, 'water': 0.8, 'air': 0.3, 'soil': 0.04, 'energy': 0.5},
    WasteType.WASTE_EXPERIMENTAL_EQUIPMENT: {'tree': 0.005, 'water': 0.5, 'air': 0.8, 'soil': 0.02, 'energy': 0.6},
    WasteType.WASTE_HEAT: {'tree': 0.003, 'water': 0.3, 'air': 0.4, 'soil': 0.05, 'energy': 1},
    WasteType.WASTE_PAPER: {'tree': 0.015, 'water': 0.3, 'air': 0.2, 'soil': 0.01, 'energy': 0.3},
    WasteType.HOUSEHOLD_WASTE: {'tree': 0.015, 'water': 0.3, 'air': 0.3, 'soil': 0.02, 'energy': 0.3},
}

compound_contribution = [
    # 水 富营养物
    'NH4',
    'NO3',
    'PO4',
    'SO4',

    # 土壤 重金属含量
    'Pb',
    'Cd',
    'Hg',
    'Cr',
    'Cu',

    # 有机物
    'Benzene',  # 有机物苯
    'Phenol',  # 酚
    'Chlorinated',  # 氯代
]
simple_substance_contribution = [

    'CO2',

    'Plastics',  # 微塑料
    'NO',
    'NO2',
    'SO2',
    'PM10',
    'PM2.5',

]


@individual.route('/contribution')
def contribution():
    global all_orders, orders_by_day
    user = g.user
    uid = user.UID
    today = datetime.now()
    contribution_dict = {'tree': 0, 'water': 0, 'air': 0, 'soil': 0, 'energy': 0}
    waste_dict = {'CO2': 0,
                  'NH4-': 0, 'NO3-': 0, 'PO43-': 0, 'SO42-': 0, 'Benzene': 0, 'Phenol': 0, 'Chlorinated': 0,
                  'Plastics': 0,
                  'NO': 0, 'NO2': 0, 'SO2': 0, 'PM10': 0, 'PM2.5': 0,
                  'Pb2+': 0, 'Cd2+': 0, 'Hg+': 0, 'Cr6+': 0, 'Cu2+': 0
                  }
    if user is not None:
        all_orders = Order.query.filter_by(UID=uid).all()
        current_year = today.year
        current_month = today.month
        orders_by_day = {}  # 用于存储每个日期的订单数量，格式为 {日期: 订单数量}

        for order in all_orders:
            wasteType = order.wasteType
            weight = order.weight
            contribution_weight = order.weight * order.multiplier

            contribution_ratios = waste_contribution.get(wasteType)

            for key, value in contribution_ratios.items():
                contribution_dict[key] += contribution_weight * value

            # 处理订单属性
            if order.attribution:
                attribution_dict = parse_attribution(order.attribution, simple_substance_contribution,
                                                     compound_contribution)
                # 更新waste_dict中的属性值
                for attr, ratio in attribution_dict.items():
                    for category in waste_dict.keys():
                        if attr in category:
                            waste_dict[category] += weight * ratio
            order_date = order.date
            if ((order_date.year == current_year and order_date.month <= current_month)
                    or (order_date.year == current_year - 1 and order_date.month >= current_month)):
                date_str = order_date.strftime('%Y-%m-%d')
                orders_by_day[date_str] = orders_by_day.get(date_str, 0) + 1
    for key, value in contribution_dict.items():
        contribution_dict[key] = round(value)
    print(contribution_dict)
    print(waste_dict)
    filtered_waste_dict = [{'attr': k, 'v': v} for k, v in waste_dict.items() if v != 0]
    combined_dict = {'normal': contribution_dict, 'a': filtered_waste_dict}
    print(combined_dict)
    return render_template('individual/contribution.html', all_orders=all_orders, orders_by_day=orders_by_day,
                           waste_dict=combined_dict)


def parse_attribution(attribution_str, simple_keywords, compound_keywords):
    attribution_dict = {}

    attribution_list = attribution_str.strip().split(' ')
    # print("attribution_list", attribution_list)
    for attribution in attribution_list:
        # 将化学式和百分比分开
        chemical_formula, percentage = attribution.split(":")
        print("chemical_formula", chemical_formula)

        for keyword in simple_keywords:

            if chemical_formula == keyword:
                contribution_ratio = float(percentage.strip('%')) / 100
                if keyword in attribution_dict:
                    attribution_dict[keyword] += contribution_ratio
                else:
                    attribution_dict[keyword] = contribution_ratio

        for keyword in compound_keywords:
            if keyword in chemical_formula and keyword!=chemical_formula:
                contribution_ratio = float(percentage.strip('%')) / 100
                if keyword in attribution_dict:
                    attribution_dict[keyword] += contribution_ratio
                else:
                    attribution_dict[keyword] = contribution_ratio

    print(attribution_dict)
    return attribution_dict


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

    # 读取上传的图像文件
    image_data = file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image_np = np.array(image)

    images_base64_list, labels = perform_analysis(image_np)
    if len(images_base64_list) != 0 and len(labels) != 0:
        return jsonify({'message': 'successful', 'images': images_base64_list, 'labels': labels}), 200
    else:
        return jsonify({'message': 'analysis failed'}), 200


def perform_analysis(image):
    model = YOLO("App/best.pt")

    # 对传入的图像进行预测
    results = model.predict(image)

    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    labels = results[0].boxes.cls.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy()

    extracted_images = []
    extracted_labels = []

    for index, (box, label, conf) in enumerate(zip(boxes, labels, confs)):
        if index >= 9:
            break
        x1, y1, x2, y2 = box

        label_name = model.names[label]
        label_text = f"{label_name}"
        # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # cv2.putText(image, label_text, (x1, y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        extracted_image = cv2.resize(cv2.cvtColor(image[y1:y2, x1:x2].copy(), cv2.COLOR_BGR2RGB), (200, 200),
                                     interpolation=cv2.INTER_CUBIC)
        extracted_images.append(extracted_image)
        extracted_labels.append(label_text)

    # 将提取的图像转换为 Base64 字符串
    images_base64_list = []
    for img in extracted_images:
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_byte_arr = io.BytesIO()
        img_pil.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img_base64 = base64.b64encode(img_byte_arr.read()).decode('utf-8')
        images_base64_list.append(img_base64)

    return images_base64_list, extracted_labels
