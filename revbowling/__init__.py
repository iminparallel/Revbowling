from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from revbowling.config import Config
from os import path
DB_NAME = "site.db"
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_database(app):
    if not path.exists("revbowling/" + DB_NAME):
        db.create_all()
        print("Created database!")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .models import User, Post, Comment, Like, Chat
    with app.app_context():
        create_database(app)
        

    from revbowling.users.routes import users
    from revbowling.posts.routes import posts
    from revbowling.main.routes import main
    from revbowling.chat.routes import chat
    from revbowling.errors.handlers import errors

    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(chat)
    app.register_blueprint(errors)


    return app
