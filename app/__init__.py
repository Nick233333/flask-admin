from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://nick:nick@localhost/flask-movie"
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
# 使用app对象，调用register_blueprint函数进行蓝图的注册
# 第一个参数是蓝图，第二个参数是url地址的前缀。通过地址前缀划分前后台的路由
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")

@app.errorhandler(404)
def page_not_found(error):
    # 404
    return render_template("home/404.html"), 404

