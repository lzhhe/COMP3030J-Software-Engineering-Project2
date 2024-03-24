# 冶金：重金属废水，废气，矿物残渣
# 高端机械设备制造：切削液和金属屑，塑料和复合材料切割废料，油漆溶剂和废漆
# 复合材料制造：粉尘和所需化学品
# 新能源：化学推进剂和燃料残留物
# 自动化系统：废弃电子元器件
# 设备维护：液压油和润滑油废料
# 实验室：有害化学品和废弃实验器材
# 行政：废纸和生活垃圾
# 数据中心：废热
import yaml

# 加载YAML文件
with open('waste.yaml', 'r') as file:
    data = yaml.safe_load(file)


# attribute_Dict 有这严格的定义，需要有对应的模板进行规范，否则报错
class Waste:
    def __init__(self, name, department, generated_date, attribute_Dict):
        self.name = name
        self.department = department
        self.generated_date = generated_date
        self.attribute_Dict = attribute_Dict


class SolidWaste(Waste):
    def __init__(self, name, department, generated_date, attribute_Dict):
        super().__init__(name, department, generated_date,attribute_Dict)


class LiquidWaste(Waste):
    def __init__(self, name, department, generated_date, attribute_Dict):
        super().__init__(name, department, generated_date,attribute_Dict)



class GaseousWaste(Waste):
    def __init__(self, name, department, generated_date, attribute_Dict):
        super().__init__(name, department, generated_date,attribute_Dict)
