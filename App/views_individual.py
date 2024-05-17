import os
import random
import string

import cv2
import numpy as np
from ultralytics import YOLO

from .models import *
from .views_utils import *

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


def predict_image(image):
    # 加载YOLO模型
    model = YOLO("pt_file")

    # 对传入的图像进行预测
    results = model.predict(image, persist=False)

    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    labels = results[0].boxes.cls.cpu().numpy()
    confs = results[0].boxes.conf.cpu().numpy()
    for box, label, conf in zip(boxes, labels, confs):
        x1, y1, x2, y2 = box
        label_text = f"Label: {label} Confidence: {conf:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image


@individual.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # 读取上传的图像文件
        nparr = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result_image = predict_image(image)

        _, img_encoded = cv2.imencode('.jpg', result_image)
        img_bytes = img_encoded.tobytes()

        return img_bytes
