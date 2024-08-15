
from flask import Blueprint, render_template
from revbowling.models import Chat
from flask_login import current_user

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)
    return render_template('errors/404.html', rooms=rooms), 404


@errors.app_errorhandler(403)
def error_403(error):
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)

    return render_template('errors/403.html', rooms=rooms), 403


@errors.app_errorhandler(500)
def error_500(error):
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)

    return render_template('errors/500.html', rooms=rooms), 500
