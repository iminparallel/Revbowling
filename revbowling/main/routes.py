from flask import render_template, request, Blueprint
from revbowling.models import Post, Comment, Chat
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    #rooms = chatInfo.query(chatInfo.rooms.like(f'%{current_user.username}%')).distinct.all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)

    return render_template('home.html', posts=posts, rooms=rooms)

@main.route("/about")
@login_required
def about():
    user = current_user.username
    rooms = Chat.query.filter(Chat.rooms.like(f'%{user}%')).order_by(Chat.date_created.desc()).group_by(Chat.rooms)

    return render_template('about.html', title='About', rooms=rooms)
