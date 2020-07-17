# models.py

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    last_login = db.Column(db.Text)
    last_request = db.Column(db.Text)
    posts = db.relationship('Post', backref='user')
    likes = db.relationship('Like', backref='user')

    # def __init__(self, first_name, last_name, email):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #
    # def __repr__(self):
    #     return '<User: {} {} {}>'.format(
    #         self.first_name, self.last_name, self.email)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.Text, nullable=False)
    # every post should have an author
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # post can have multiple likes, from different users
    post_likes = db.relationship('Like', backref='post')


class Like(db.Model):
    __tablename__ = 'like'
    # table likes stores info about all likes
    # consists of, post id, user id, time_when_user_liked,
    id = db.Column(db.Integer, primary_key=True)
    liked = db.Column(db.Boolean, nullable=False)
    time_when_user_liked = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
