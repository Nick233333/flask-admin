import os
import redis
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


app = Flask(__name__, template_folder='templates')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://nick:nick@localhost/flask-movie"
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'flask-movie'
app.config['UPLOAD_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
db = SQLAlchemy(app)

app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
app.config['SESSION_PERMANENT'] = False  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_USE_SIGNER'] = True  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_KEY_PREFIX'] = 'flask:'  # 保存到session中的值的前缀
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port='6379', password='redis') # 用于连接redis的配置

Session(app)


from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
from app.api import api as api_blueprint
# 使用app对象，调用register_blueprint函数进行蓝图的注册
# 第一个参数是蓝图，第二个参数是url地址的前缀。通过地址前缀划分前后台的路由
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(api_blueprint, url_prefix="/api")

@app.errorhandler(404)
def page_not_found(error):
    # 404
    return render_template("home/404.html"), 404

