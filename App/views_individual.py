import base64
import io

import cv2
import numpy as np
from PIL import Image

import random
import string

from ultralytics import YOLO

from .models import *
from .views_utils import *

individual = Blueprint('individual', __name__, url_prefix='/individual')  # individual is name of blueprint

'''拯救树 棵，保护水 升，净化空气 立方米，增加土壤肥沃 吨，节约能源 千瓦时，CO2 减排量 公斤'''
waste_contribution = {
    WasteType.HEAVY_METAL_WASTEWATER: {'tree': 0.02, 'water': 5, 'air': 3, 'soil': 0.01, 'energy': 1, 'co2': 1.5},
    WasteType.EXHAUST_GAS: {'tree': 0.01, 'water': 2, 'air': 10, 'soil': 0.005, 'energy': 0.5, 'co2': 5},
    WasteType.MINERAL_RESIDUE: {'tree': 0.02, 'water': 8, 'air': 1, 'soil': 0.02, 'energy': 2, 'co2': 2},
    WasteType.CUTTING_FLUID: {'tree': 0.03, 'water': 10, 'air': 4, 'soil': 0.04, 'energy': 3, 'co2': 2},
    WasteType.METAL_CHIPS: {'tree': 0.03, 'water': 6, 'air': 3, 'soil': 0.03, 'energy': 2, 'co2': 1.5},
    WasteType.PLASTIC: {'tree': 0.02, 'water': 4, 'air': 1, 'soil': 0.02, 'energy': 1.5, 'co2': 1.5},
    WasteType.COMPOSITE_MATERIAL_CUTTING_WASTE: {'tree': 0.03, 'water': 10, 'air': 4, 'soil': 0.04, 'energy': 3,
                                                 'co2': 2},
    WasteType.WASTE_PAINT: {'tree': 0.02, 'water': 5, 'air': 3, 'soil': 0.01, 'energy': 1, 'co2': 1.5},
    WasteType.DUST: {'tree': 0.01, 'water': 2, 'air': 10, 'soil': 0.005, 'energy': 0.5, 'co2': 5},
    WasteType.CHEMICALS: {'tree': 0.04, 'water': 10, 'air': 4, 'soil': 0.04, 'energy': 3, 'co2': 2},
    WasteType.CATALYZER: {'tree': 0.05, 'water': 8, 'air': 3, 'soil': 0.04, 'energy': 5, 'co2': 5},
    WasteType.CHEMICAL_PROPELLANTS: {'tree': 0.05, 'water': 8, 'air': 3, 'soil': 0.04, 'energy': 5, 'co2': 5},
    WasteType.FUEL_RESIDUES: {'tree': 0.02, 'water': 8, 'air': 1, 'soil': 0.02, 'energy': 8, 'co2': 5},
    WasteType.DISCARDED_ELECTRONIC_COMPONENTS: {'tree': 0.04, 'water': 5, 'air': 3, 'soil': 0.1, 'energy': 2,
                                                'co2': 1.5},
    WasteType.HYDRAULIC_OIL: {'tree': 0.04, 'water': 10, 'air': 4, 'soil': 0.04, 'energy': 3, 'co2': 2},
    WasteType.LUBRICANT_WASTE: {'tree': 0.04, 'water': 10, 'air': 4, 'soil': 0.04, 'energy': 3, 'co2': 2},
    WasteType.HAZARDOUS_CHEMICALS: {'tree': 0.05, 'water': 8, 'air': 3, 'soil': 0.04, 'energy': 5, 'co2': 5},
    WasteType.WASTE_EXPERIMENTAL_EQUIPMENT: {'tree': 0.05, 'water': 5, 'air': 8, 'soil': 0.02, 'energy': 6, 'co2': 2},
    WasteType.WASTE_HEAT: {'tree': 0.03, 'water': 3, 'air': 4, 'soil': 0.05, 'energy': 10, 'co2': 8},
    WasteType.WASTE_PAPER: {'tree': 0.15, 'water': 3, 'air': 2, 'soil': 0.01, 'energy': 3, 'co2': 3},
    WasteType.HOUSEHOLD_WASTE: {'tree': 0.15, 'water': 3, 'air': 3, 'soil': 0.02, 'energy': 3, 'co2': 3},
}

attribution_contribution = {
    'CO2': {'tree': 3, 'water': 2, 'air': 4, 'soil': 1, 'energy': 2, 'co2': 10},
    'SO2': {'tree': 2, 'water': 2, 'air': 5, 'soil': 2, 'energy': 1, 'co2': 3},
    'J': {'tree': 1, 'water': 1, 'air': 1, 'soil': 3, 'energy': 20, 'co2': 2},
    'N2': {'tree': 2, 'water': 1, 'air': 4, 'soil': 2, 'energy': 5, 'co2': 3},
    'CL2': {'tree': 1, 'water': 2, 'air': 5, 'soil': 2, 'energy': 4, 'co2': 4},
    'FE': {'tree': 1, 'water': 1, 'air': 2, 'soil': 1, 'energy': 8, 'co2': 1},
    'S': {'tree': 1, 'water': 1, 'air': 2, 'soil': 1, 'energy': 5, 'co2': 2},
    'C': {'tree': 3, 'water': 1, 'air': 2, 'soil': 1, 'energy': 6, 'co2': 6},
}


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
    model = YOLO("App/huazhongv8.pt")

    # 对传入的图像进行预测
    results = model.predict(image)

    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    labels = results[0].boxes.cls.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy()

    extracted_images = []
    extracted_labels = []

    for index, (box, label, conf) in enumerate(zip(boxes, labels, confs)):
        if index >= 10:
            break
        x1, y1, x2, y2 = box

        label_name = model.names[label]
        label_text = f"{label_name}"
        # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # cv2.putText(image, label_text, (x1, y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        extracted_image = cv2.resize(image[y1:y2, x1:x2].copy(), (224, 224), interpolation=cv2.INTER_CUBIC)
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
