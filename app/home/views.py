from flask import render_template, url_for, redirect
from . import home


@home.route("/")
def index():
    # 列表
    return render_template("home/index.html")


@home.route("/animation/")
def animation():
    # 动画
    return render_template("home/animation.html")


@home.route("/login/")
def login():
    # 登录
    return render_template("home/login.html")


@home.route("/logout/")
def logout():
    # 退出
    return redirect(url_for('home.login'))


@home.route("/register/")
def register():
    # 注册
    return render_template("home/register.html")


@home.route("/loginlog/")
def loginlog():
    # 登录日志
    return render_template("home/loginlog.html")


@home.route("/user/")
def user():
    # 用户中心
    return render_template("home/user.html")


@home.route("/pwd/")
def pwd():
    # 修改密码
    return render_template("home/pwd.html")


@home.route("/comments/")
def comments():
    # 评论
    return render_template("home/comments.html")


@home.route("/moviecol/")
def moviecol():
    # 收藏电影
    return render_template("home/moviecol.html")


@home.route("/search/")
def search():
    # 搜索
    return render_template("home/search.html")


@home.route("/play/")
def play():
    # 播放
    return render_template("home/play.html")



