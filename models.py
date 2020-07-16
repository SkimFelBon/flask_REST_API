# models.py

from app import db
from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    last_login = db.Column(db.Text)
    last_request = db.Column(db.Text)
    posts = db.relationship('Post', backref='user')
    likes = db.relationship('Like', backref='user')


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.Text, nullable=False)
    # every post should have an author
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # post can have multiple likes, from different users
    post_likes = db.relationship('Like', backref='post')


class Like(db.Model):
    __tablename__ = 'like'
    # table likes stores info about all likes
    # consists of, post id, user id, time_when_user_liked,
    id = db.Column(db.Integer, primary_key=True)
    liked = db.Column(db.Boolean, nullable=False)
    time_when_user_liked = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
