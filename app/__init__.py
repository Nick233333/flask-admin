# 从前台，后台模块中导入我们的蓝图对象
from flask import Flask
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app = Flask(__name__)
app.debug = True


# 使用app对象，调用register_blueprint函数进行蓝图的注册
# 第一个参数是蓝图，第二个参数是url地址的前缀。通过地址前缀划分前后台的路由
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")

