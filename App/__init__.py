import datetime
import mimetypes

from flask import Flask

from .extents import init_exts
from .views_department import department
from .views_government import government
from .views_individual import individual
from .views_waste import waste
from .views_login import login
from .views_utils import utils

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
# PASSWORD = "131a2abLZH"
PASSWORD = "123456"
FLASK_DB = "waste_management"


def create_app():
    app = Flask(__name__, static_folder='static')

    # 注册蓝图
    app.register_blueprint(blueprint=login)
    app.register_blueprint(blueprint=department)
    app.register_blueprint(blueprint=government)
    app.register_blueprint(blueprint=individual)
    app.register_blueprint(blueprint=waste)
    app.register_blueprint(blueprint=utils)

    app.config['SECRET_KEY'] = 'COMP3019J'

    db_uri = f'mysql+pymysql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{FLASK_DB}?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_exts(app)
    mimetypes.add_type('application/javascript', '.js')

    return app
