from datetime import datetime

from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer

from src import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    last_seen = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User({self.id}, {self.username}, {self.email}, {self.password}, {self.image_file})'


class Post(db.Model):
    __tablename__ = "posts"
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text(60), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_post = db.Column(db.String(50), nullable=False, default='default.jpg')
    slug = db.Column(db.String(), unique=True, index=True)
    tg = db.relationship('Tg', backref='tg_post', lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'Post({self.id}, {self.title}, {self.date_posted}, {self.image_post}, {self.user_id})'


class Tg(db.Model):
    __tablename__ = 'tg'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Tg({self.id}, {self.name}, {self.post_id})'
