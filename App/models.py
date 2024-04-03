from datetime import datetime, date

from .extents import db
from enum import Enum, unique
from sqlalchemy import Column, Integer, Enum as SQLEnum
from enum import Enum, auto


@unique
class DepartmentType(Enum):
    METALLURGY = auto()  # 冶金
    EQUIPMENT_MANUFACTURING = auto()  # 高端机械设备制造
    COMPOSITE_MATERIAL = auto()  # 复合材料制造
    NEW_ENERGY = auto()  # 新能源
    AUTOMATION_SYSTEM = auto()  # 自动化系统
    MAINTENANCE = auto()  # 设备维护
    LABORATORY = auto()  # 实验室
    DATA_CENTER = auto()  # 数据中心
    OFFICE = auto()  # 行政


@unique
class WasteType(Enum):
    # 冶金类废物
    HEAVY_METAL_WASTEWATER = auto()  # 重金属废水
    EXHAUST_GAS = auto()  # 废气
    MINERAL_RESIDUE = auto()  # 矿物残渣

    # 高端机械设备制造类废物
    CUTTING_FLUID = auto()  # 切削液
    METAL_CHIPS = auto()  # 金属屑
    PLASTIC = auto()  # 塑料
    COMPOSITE_MATERIAL_CUTTING_WASTE = auto()  # 复合材料切割废料
    WASTE_PAINT = auto()  # 废漆

    # 复合材料制造类废物
    DUST = auto()  # 粉尘
    CHEMICALS = auto()  # 化学品
    CATALYZER = auto()  # 催化剂

    # 新能源类废物
    CHEMICAL_PROPELLANTS = auto()  # 化学推进剂
    FUEL_RESIDUES = auto()  # 燃料残渣

    # 自动化系统类废物
    DISCARDED_ELECTRONIC_COMPONENTS = auto()  # 废弃电子元器件

    # 设备维护类废物
    HYDRAULIC_OIL = auto()  # 液压油
    LUBRICANT_WASTE = auto()  # 润滑油废料

    # 实验室类废物
    HAZARDOUS_CHEMICALS = auto()  # 有害化学品
    WASTE_EXPERIMENTAL_EQUIPMENT = auto()  # 废弃实验器材

    # 行政类废物
    WASTE_PAPER = auto()  # 废纸
    HOUSEHOLD_WASTE = auto()  # 生活垃圾

    # 数据中心类废物
    WASTE_HEAT = auto()  # 废热


@unique
class WasteSource(Enum):
    INTERNAL = auto()  # 内部
    EXTERNAL = auto()  # 外部
    EXTERNALFREE = auto()  # 外部免费


@unique
class OrderStatus(Enum):
    UNCONFIRMED = auto()  # 未确认
    CONFIRM = auto()  # 确认
    # STORAGE = auto()  # 已经储存
    PROCESSING = auto()  # 处理中
    FINISHED = auto()
    DISCHARGED = auto()  # 已排放


@unique
class UserStatus(Enum):
    DEPARTMENT_MANAGER = auto()
    WASTE_MANAGER = auto()
    GOVERNMENT_MANAGER = auto()
    INDIVIDUAL_USER = auto()


class User(db.Model):
    __tablename__ = 'user'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    status = Column(SQLEnum(UserStatus), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.DID'), nullable=True)
    department = db.relationship('Department', backref=db.backref('user', uselist=False), lazy=True)


class Department(db.Model):
    __tablename__ = 'department'
    DID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departmentName = db.Column(db.String(200), nullable=False, unique=True)
    departmentType = db.Column(SQLEnum(DepartmentType), nullable=False)
    departmentAddress = db.Column(db.String(500), nullable=False)


class Waste(db.Model):  # 产生的废物映射部门种类
    __tablename__ = 'waste'
    WID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id唯一
    wasteType = Column(SQLEnum(WasteType), nullable=False)
    wasteDepartment = db.Column(SQLEnum(DepartmentType), nullable=True)
    wasteSource = Column(SQLEnum(WasteSource), nullable=False, default=WasteSource.INTERNAL)


class WasteStorage(db.Model):  # 储存能力
    __tablename__ = 'wasteStorage'
    WSID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wasteType = db.Column(SQLEnum(WasteType), nullable=False)  # 废弃物类型
    maxCapacity = db.Column(db.Integer, nullable=False)  # 最大存储量
    currentCapacity = db.Column(db.Integer, default=0, nullable=False)  # 当前存储量，默认为0

    def __repr__(self):
        return f'<WasteStorage {self.wasteType} max:{self.maxCapacity} current:{self.currentCapacity}>'


class ProcessCapacity(db.Model):  # 处理能力
    __tablename__ = 'processCapacity'
    PCID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wasteType = db.Column(SQLEnum(WasteType), nullable=False)  # 废弃物类型
    maxCapacity = db.Column(db.Integer, nullable=False)  # 最大同时处理量
    currentCapacity = db.Column(db.Integer, default=0, nullable=False)  # 当前处理量，默认为0

    def __repr__(self):
        return f'<ProcessCapacity {self.wasteType} max:{self.maxCapacity} current:{self.currentCapacity}>'


class Order(db.Model):  # 工单
    __tablename__ = 'order'
    OID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 工单唯一ID
    UID = db.Column(db.Integer)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)  # 工单日期，默认为当前日期
    orderName = db.Column(db.String(300), nullable=False)  # 工单名称
    wasteType = db.Column(SQLEnum(WasteType), nullable=False)  # 废弃物类型
    weight = db.Column(db.Integer, nullable=False)  # 废弃物重量
    attribution = db.Column(db.Text, nullable=False)  # 属性
    multiplier = db.Column(db.Integer, nullable=False, default=1)
    comment = db.Column(db.Text, nullable=True)  # 备注
    orderStatus = Column(SQLEnum(OrderStatus), nullable=False)  # 处理状态
    department_id = db.Column(db.Integer, db.ForeignKey('department.DID'), nullable=True)
    # 设置与Department表的关系
    department = db.relationship('Department', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order OID:{self.OID} DID:{self.DID} date:{self.date} orderName:{self.orderName}>'
