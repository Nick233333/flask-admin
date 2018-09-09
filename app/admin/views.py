import os
import uuid
from datetime import datetime

from flask import render_template, url_for, redirect, flash, session, request
from . import admin
from app.admin.forms import LoginForm, TagForm, MovieForm
from functools import wraps
from app.models import Admin, Tag, Movie
from app import db, app
from werkzeug.utils import secure_filename


def admin_login_req(f):
    # 登录装饰器
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def change_filename(filename):
    # 修改文件名称
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


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
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_login_req
def movie_add():
    # 添加电影页面
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UPLOAD_DIR']):
            # 创建一个多级目录
            os.makedirs(app.config['UPLOAD_DIR'])
            os.chmod(app.config['UPLOAD_DIR'], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        # 保存
        form.url.data.save(app.config['UPLOAD_DIR'] + url)
        form.logo.data.save(app.config['UPLOAD_DIR'] + logo)
        # url,logo为上传视频,图片之后获取到的地址
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash(u"添加电影成功！", "ok")
        return redirect(url_for('admin.movie_list', page=1))
    return render_template("admin/movie_add.html", form=form)


@admin.route("/movie/list/<int:page>/", methods=["GET"])
@admin_login_req
def movie_list(page=None):
    # 电影列表
    if page is None:
        page = 1
    # 进行关联Tag的查询,单表查询使用filter_by 多表查询使用filter进行关联字段的声明
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/movie_list.html", page_data=page_data)


@admin.route("/movie/del/<int:id>/", methods=["GET"])
@admin_login_req
def movie_del(id=None):
    # 删除电影
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash("电影删除成功", "ok")
    return redirect(url_for('admin.movie_list', page=1))


@admin.route("/movie/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
# @admin_auth
def movie_edit(id=None):
    """
    编辑电影页面
    """
    form = MovieForm()
    # 因为是编辑，所以非空验证空
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data["title"]).count()
        if movie_count == 1 and movie.title != data["title"]:
            flash(u"电影标题已经存在！", "err")
            return redirect(url_for('admin.movie_edit', id=id))
        # 创建目录
        if not os.path.exists(app.config['UPLOAD_DIR']):
            os.makedirs(app.config['UPLOAD_DIR'])
            os.chmod(app.config['UPLOAD_DIR'], "rw")
        # 上传视频
        if form.url.data != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config['UPLOAD_DIR'] + movie.url)
        # 上传图片
        if form.logo.data != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UPLOAD_DIR'] + movie.logo)

        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash(u"修改电影成功！", "ok")
        return redirect(url_for('admin.movie_list', page=1))
    return render_template("admin/movie_edit.html", form=form, movie=movie)


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
