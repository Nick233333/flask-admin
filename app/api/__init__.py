from flask import Blueprint
# 传入两个参数，一个是蓝图名称，一个是 name 值
api = Blueprint("api", __name__)
import app.api.views