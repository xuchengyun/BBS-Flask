from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    flash,
)

from models.user import User
from models.topic import Topic
from models.board import Board
from utils import log
from werkzeug.utils import secure_filename
from models.user import User
from config import user_file_director
import os

main = Blueprint('index', __name__)


def current_user():
    # find user_id from session, if not exist set to -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    bs = Board.all()
    ms = Topic.find_all(__sort='created_time', __order='reverse')
    print('ms ', ms)
    if u is not None:
        return redirect(url_for('topic.index'))
    else:
        return render_template("index.html", ms=ms, bs=bs, u=u)


@main.route("/signup")
def signup():
    return render_template("signup.html")


@main.route("/signin")
def signin():
    return render_template("signin.html")


@main.route("/register", methods=['GET', 'POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    if u is not None:
        flash("You have sucessfully signed up")
        # automatically login
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))
    else:
        flash("username is already exist, please try again!")
        return redirect(url_for('.signup'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        flash('Sorry, we couldn\'t find you in our database, please register first')
        return redirect(url_for('.signin'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".profile"))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for(".index"))


# send_from_directory
# nginx static file
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)
