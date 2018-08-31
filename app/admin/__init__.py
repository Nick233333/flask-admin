from flask import Blueprint
# 传入两个参数，一个是蓝图名称，一个是 name 值
admin = Blueprint("admin", __name__)
import app.admin.views