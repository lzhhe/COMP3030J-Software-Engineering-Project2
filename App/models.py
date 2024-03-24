from datetime import datetime, date
from .extents import db
from enum import Enum, unique
from sqlalchemy import Column, Integer, Enum as SQLEnum
from enum import Enum, auto


@unique
class DepartmentKind(Enum):
    METALLURGY = auto()  # 冶金
    EQUIPMENT_MANUFACTURING = auto()  # 高端机械设备制造
    COMPOSITE_MATERIAL = auto()  # 复合材料制造
    NEW_ENERGY = auto()  # 新能源
    AUTOMATION_SYSTEM = auto()  # 自动化系统
    MAINTENANCE = auto()  # 设备维护
    LABORATORY = auto()  # 实验室
    DATA_CENTER = auto()  # 行政
    OFFICE = auto()  # 数据中心


@unique
class WasteKind(Enum):
    METALLURGY = ["heavy metal wastewater", "exhaust gas", "mineral residue"]  # 冶金：重金属废水，废气，矿物残渣
    EQUIPMENT_MANUFACTURING = ["cutting fluid", "metal chips", "plastic", "composite material cutting waste",
                               "paint solvents", "waste paint"]  # 高端机械设备制造：切削液和金属屑，塑料和复合材料切割废料，油漆溶剂和废漆
    COMPOSITE_MATERIAL = ["dust", "required chemicals"]  # 复合材料制造：粉尘和所需化学品
    NEW_ENERGY = ["chemical propellants", "fuel residues"]  # 新能源：化学推进剂和燃料残留物
    AUTOMATION_SYSTEM = ["discarded electronic components"]  # 自动化系统：废弃电子元器件
    MAINTENANCE = ["hydraulic oil", "lubricant waste"]  # 设备维护：液压油和润滑油废料
    LABORATORY = ["Hazardous chemicals", "waste experimental equipment"]  # 实验室：有害化学品和废弃实验器材
    DATA_CENTER = [" Waste paper", "household waste"]  # 行政：废纸和生活垃圾
    OFFICE = ["waste heat"]  # 数据中心：废热


@unique
class OrderStatus(Enum):
    UNREGISTERED = auto()  # 未登记
    UNCONFIRMED = auto()  # 未确认
    CONFIRM = auto()  # 确认
    UNTRANSPORTED = auto()  # 未运输
    TRANSPORTATION = auto()  # 运输途中
    UNPROCESSED = auto()  # 未处理
    PROCESSED = auto()  # 已处理
    DISCHARGED = auto()  # 已排放


@unique
class UserStatus(Enum):
    DEPARTMENT_MANAGER = auto()
    WASTE_MANAGER = auto()
    GOVERNMENT_MANAGER = auto()
    INDIVIDUAL_USER = auto()


class User(db.Model):
    __tablename__ = 'user'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id唯一
    username = db.Column(db.String(30), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(256), nullable=False)  # 密码
    email = db.Column(db.String(100), nullable=False)  # 邮箱
    status = Column(SQLEnum(UserStatus), nullable=False)
    department = db.Column(db.String(100), nullable=True)


class Department(db.Model):
    __tablename__ = 'department'
    DID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id唯一
    departmentName = db.Column(db.String(200), nullable=False)
    departmentKind = db.Column(SQLEnum(DepartmentKind), nullable=False)
    departmentAddress = db.Column(db.String(500), nullable=False)
    managerId = db.Column(db.Integer, db.ForeignKey('user.UID'), nullable=False)  # 添加部门经理外键字段
    manager = db.relationship('User', backref='managed_departments', lazy=True)  # 设置relationship (如果需要的话)


class Order(db.Model):  # 提交需要处理的表单
    __tablename__ = 'order'
    OID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id唯一
    orderName = db.Column(db.String(100), nullable=False)
