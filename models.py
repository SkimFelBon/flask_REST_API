# models.py

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    last_login = db.Column(db.DateTime)
    last_request = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='user')
    likes = db.relationship('Like', backref='user')

    def __repr__(self):
        return '<User: {} {} {}>'.format(
            self.first_name, self.last_name, self.email)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
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
    time_when_user_liked = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
