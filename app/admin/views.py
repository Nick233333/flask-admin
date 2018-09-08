from flask import render_template, url_for, redirect, flash, session, request
from . import admin
from app.admin.forms import LoginForm, TagForm
from functools import wraps
from app.models import Admin, Tag
from app import db, app


def admin_login_req(f):
    # 登录装饰器
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 路由定义使用装饰器进行定义
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


@admin.route("/login/", methods=["GET", "POST"])
def login():
    # 后台登录
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash(u"密码错误!", "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout")
def logout():
    # 后台注销登录
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


@admin.route("/pwd/")
def pwd():
    # 后台密码修改
    return render_template("admin/pwd.html")


@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_req
def tag_add():
    # 标签添加
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash(u"标签已存在", "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash(u"标签添加成功", "ok")
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_login_req
def tag_del(id=None):
    # 标签删除
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash(u"标签<<{0}>>删除成功".format(tag.name), "ok")
    return redirect(url_for("admin.tag_list", page=1))


@admin.route("/tag/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def tag_edit(id=None):
    # 标签编辑
    form = TagForm()
    form.submit.label.text = u"修改"
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and tag_count == 1:
            flash(u"标签已存在", "err")
            return redirect(url_for("admin.tag_edit", id=tag.id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash(u"标签修改成功", "ok")
        redirect(url_for("admin.tag_edit", id=tag.id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_login_req
def tag_list(page=None):
    # 标签列表
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=1)
    return render_template("admin/tag_list.html", page_data=page_data)


@admin.route("/movie/add/")
def movie_add():
    # 编辑电影页面
    return render_template("admin/movie_add.html")


@admin.route("/movie/list/")
def movie_list():
    # 电影列表页面
    return render_template("admin/movie_list.html")


@admin.route("/preview/add/")
def preview_add():
    # 上映预告添加
    return render_template("admin/preview_add.html")


@admin.route("/preview/list/")
def preview_list():
    # 上映预告列表
    return render_template("admin/preview_list.html")


@admin.route("/user/list/")
def user_list():
    # 会员列表
    return render_template("admin/user_list.html")


@admin.route("/user/view/")
def user_view():
    # 会员
    return render_template("admin/user_view.html")


@admin.route("/comment/list/")
def comment_list():
    # 评论列表
    return render_template("admin/comment_list.html")


@admin.route("/moviecol/list/")
def moviecol_list():
    # 电影收藏
    return render_template("admin/moviecol_list.html")


@admin.route("/oplog/list/")
def oplog_list():
    # 操作日志管理
    return render_template("admin/oplog_list.html")


@admin.route("/adminloginlog/list/")
def adminloginlog_list():
    # 管理员日志列表
    return render_template("admin/adminloginlog_list.html")


@admin.route("/userloginlog/list/")
def userloginlog_list():
    # 会员日志列表
    return render_template("admin/userloginlog_list.html")


@admin.route("/auth/add/")
def auth_add():
    # 添加权限
    return render_template("admin/auth_add.html")


@admin.route("/auth/list/")
def auth_list():
    # 权限列表
    return render_template("admin/auth_list.html")


@admin.route("/role/add/")
def role_add():
    # 添加角色
    return render_template("admin/role_add.html")


@admin.route("/role/list/")
def role_list():
    # 角色列表
    return render_template("admin/role_list.html")


@admin.route("/admin/add/")
def admin_add():
    # 添加管理员
    return render_template("admin/admin_add.html")


@admin.route("/admin/list/")
def admin_list():
    # 管理员列表
    return render_template("admin/admin_list.html")
