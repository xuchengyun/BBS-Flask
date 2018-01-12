from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    u = current_user()
    if u.role == 1:
        return render_template('board/admin_index.html')
    else:
        return redirect(url_for('topic.index'))


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    if u.role == 1:
        m = Board.new(form)
    return redirect(url_for('topic.index'))


@main.route("/delete", methods=["POST"])
def delete():
    pass

