from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from revbowling import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    chat = db.relationship('Chat', backref='user', lazy=True)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', cascade="all,delete", backref='post')
    likes = db.relationship('Like', cascade="all,delete", backref='post')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)
    
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message =  db.Column(db.String(150), nullable=False)
    rooms =  db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    author  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   

  #  class Rooms(db.Model):
   #     id = db.Column(db.Integer, primary_key=True)
    #    message =  db.Column(db.String(150), nullable=False)
     #    
      #  date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
       # author  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    