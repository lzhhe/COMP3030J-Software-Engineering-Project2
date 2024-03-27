import datetime
import mimetypes

from flask import Flask, request, session
from flask_babel import Babel

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
    # 应用配置
    app.config['SECRET_KEY'] = 'COMP3030J'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

    babel = Babel(app)

    def get_locale():
        # 检查用户是否通过界面选择了语言，并在 session 中存储了该选择
        return session.get('language', request.accept_languages.best_match(['en', 'zh_Hans_CN']))

    babel.init_app(app, locale_selector=get_locale)

    # 注册蓝图
    app.register_blueprint(blueprint=login)
    app.register_blueprint(blueprint=department)
    app.register_blueprint(blueprint=government)
    app.register_blueprint(blueprint=individual)
    app.register_blueprint(blueprint=waste)
    app.register_blueprint(blueprint=utils)

    db_uri = f'mysql+pymysql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{FLASK_DB}?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_exts(app)
    mimetypes.add_type('application/javascript', '.js')

    return app
