from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
    flash,
)

from routes import *
from models.topic import Topic
from models.board import Board
import time
main = Blueprint('topic', __name__)

import uuid
csrf_tokens = dict()


@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.find_all(__sort='created_time', __order='reverse')
    else:
        ms = Topic.find_all(board_id=board_id, __sort='created_time', __order='reverse')
    token = str(uuid.uuid4())
    u = current_user()
    bs = Board.all()
    if u is not None:
        csrf_tokens['token'] = u.id
        return render_template("topic/index.html", ms=ms, token=token, bs=bs, u=u)
    return redirect('/')


@main.route('/<int:id>')
def detail(id):
    t = time.time()
    m = Topic.get(id)
    bid = m.board_id
    uid = m.user_id
    b = Board.find_by(id=bid)
    u = User.find_by(id=uid)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, u=u, b=b, t=t)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():

    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    if int(u.role) != 1: # judge if it is administrator
        # 判断 token 是否是我们给的
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            if u is not None:
                print('删除 topic 用户是', u, id)
                Topic.delete(id)
                return redirect(url_for('.index'))
            else:
                abort(404)
        else:
            abort(403)
    else:
        Topic.delete(id)
        return redirect(url_for('.index'))


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)


@main.route('/logout')
def logout():
    if current_user() is None:
        flash('You can\'t log out if you weren\'t logged in to start with!')
    else:
        session.clear()
        flash('You were successfully logged out!')
    return redirect('/signin')



