from flask import Flask, session, g, request, jsonify, redirect, url_for, send_from_directory, make_response
from flask_babel import Babel, gettext as _
from App import create_app
from App.extents import db
from App.models import User

app = create_app()

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

babel = Babel(app)


def get_locale():
    # 检查用户是否通过界面选择了语言，并在 session 中存储了该选择
    return session.get('language', request.accept_languages.best_match(['en']))


babel.init_app(app, locale_selector=get_locale)


#
# 这一块是为了实现用户登录后，自动获取用户信息，并将其存储在全局变量g中，供模板文件使用
# 并且是确保用户登录后才能访问某些界面，否则会重定向到登录页面
@app.before_request
def my_before():
    uid = session.get('UID')
    if uid:
        user = db.session.get(User, uid)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


# 全局user变量
@app.context_processor
def my_context():
    return {'user': g.user}


#
#
# # 根据不同的用户状态，返回不同的上级页面
# @app.route('/back')
# def back():
#     # 检查用户是否登录
#     if g.user:
#         if g.user.status == 0:
#             return redirect(url_for('cal_a.adminView'))
#         if g.user.status == 1:
#             # 从会话中获取上一个子页面的标识
#             last_page = session.get('last_page', 'yearView')
#
#             # 根据上一个子页面的标识来决定重定向到哪个页面
#             if last_page == 'weekView':
#                 return redirect(url_for('cal_u.weekView'))
#             elif last_page == 'monthView':
#                 return redirect(url_for('cal_u.monthView'))
#             elif last_page == 'yearView':
#                 return redirect(url_for('cal_u.yearView'))
#         if g.user.status == 2:
#             return redirect(url_for('cal_t.teacherView'))
#     else:
#         return redirect(url_for('cal_u.main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
