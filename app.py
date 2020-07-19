# app.py
# RE.S.T. Representational State Transfer
from flask import Flask, request, jsonify, json, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from authlib.jose import jwt
from datetime import datetime, timedelta
from functools import wraps
import config
import base64
app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
# TODO: Use flask_marshmallow
db = SQLAlchemy(app)

from models import User, Post, Like
from schemas import UserSchema, PostSchema, LikeSchema

user_schema = UserSchema()
post_schema = PostSchema()
like_schema = LikeSchema()


@app.errorhandler(409)
def error_conflict(e):
    return jsonify(error=str(e)), 409


@app.errorhandler(401)
def error_unauthorized(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(400)
def error_bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(422)
def error_unprocessable_entity(e):
    return jsonify(error=str(e)), 422


@app.after_request
def update_user_last_request(response):
    """Function used to update time of users last_request"""
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return response
    header, payload, signature = token.split('.')
    bytes_payload = base64.b64decode(payload)
    dict_payload = json.loads(bytes_payload)
    expire_at = datetime.utcfromtimestamp(dict_payload['exp'])
    curr_time = datetime.utcnow()
    if expire_at < curr_time:
        return response
    user = User.query.get(dict_payload['sub'])
    user.last_request = curr_time
    db.session.commit()
    return response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # TODO: improve response descriptions?
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(abort(401, description="Token is invalid"))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as error:
            app.logger.info(error)
            return jsonify(abort(401, description="Token is invalid"))
        # also check token expiretion date
        expire_at = datetime.utcfromtimestamp(data['exp'])
        if expire_at < datetime.utcnow():
            return jsonify(abort(401, description="Token is invalid"))
        current_user = User.query.filter_by(id=data['sub']).first()
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/users/<int:prim_key>')
@token_required
def get_user_temp(current_user, prim_key):
    user = user_schema.dump(User.query.get(prim_key))
    return jsonify({"user": user})


@app.route('/api/signup', methods=['POST'])
def signup():
    # validate input
    json_data = request.get_json()
    if not json_data:
        return abort(400)
    try:
        data = user_schema.load(json_data)
    except ValidationError as error:
        app.logger.info(error)
        return abort(422)
    user_exist = User.query.filter(User.email == data['email']).first()
    if user_exist:
        return jsonify(
            abort(409, description="User with such email already exist"))
    hashed_pass = generate_password_hash(data['password'], method='sha256')
    new_user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=hashed_pass)
    db.session.add(new_user)
    db.session.commit()
    user = user_schema.dump(User.query.get(new_user.id))
    return jsonify({'message': 'Created new User.', "user": user})


@app.route('/api/login', methods=['POST'])
def login():
    """Logins user"""
    json_data = request.get_json()
    if not json_data:
        return abort(400)
    try:
        data = user_schema.load(json_data)
    except ValidationError as error:
        app.logger.info(error)
        return abort(422)
    email, password = data['email'], data['password']
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(
            abort(409, description="User with such email doesn't exist"))
    if not check_password_hash(user.password, password):
        return jsonify(abort(401))
    secret_key = app.config['SECRET_KEY']
    header = {'alg': 'HS256', 'typ': 'JWT'}
    last_login = datetime.utcnow()
    expire_at = last_login + timedelta(seconds=app.config['TOKEN_EXP'])
    payload = {'iss': 'Authlib', 'sub': user.id, 'exp': expire_at}
    signed_token = jwt.encode(header, payload, secret_key)
    user.last_login = last_login
    db.session.commit()
    return jsonify({"token": signed_token.decode('utf-8')})


@app.route('/api/post', methods=['POST'])
@token_required
def post(current_user):
    """Leave post"""
    json_data = request.get_json()
    if not json_data:
        return abort(400)
    try:
        data = post_schema.load(json_data)
    except ValidationError as error:
        app.logger.info(error)
        return abort(422)
    title, desc = data
    new_post = Post(title=title,
                    description=desc,
                    created=datetime.utcnow(),
                    author_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    post = post_schema.dump(Post.query.get(new_post.id))
    return jsonify({'message': 'Created new post.', "post": post})


@app.route('/api/like/<int:post_id>', methods=['PUT'])
@token_required
def like(current_user, post_id):
    # TODO: maybe replace like/unlike with single route that can handle
    # both requests, so I can supply specific schema to every route?
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify(
            abort(409, description="Post with such id doesn't exist"))
    like_exist = Like.query.filter_by(user_id=current_user.id,
                                      post_id=post_id
                                      ).first()
    if like_exist:
        # if like exist, check if user already liked post?
        if like_exist.liked:
            return jsonify(
                abort(409, description="Post already liked"))
        # if user previosly disliked and want to like again: update record
        like_exist.liked = True
        like_exist.time_when_user_liked = datetime.utcnow()
        db.session.commit()
    else:
        # create record in like table
        new_like = Like(
                    liked=True,
                    time_when_user_liked=datetime.utcnow(),
                    user_id=current_user.id,
                    post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
    return jsonify({"message": "Liked post"}), 201


@app.route('/api/unlike/<int:post_id>', methods=['PUT'])
@token_required
def unlike(current_user, post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify(
            abort(409, description="Post with such id doesn't exist"))
    # check if like exist
    like_exist = Like.query.filter_by(user_id=current_user.id,
                                      post_id=post_id
                                      ).first()
    if like_exist:
        if not like_exist.liked:
            return jsonify(
                abort(409, description="Post already unliked"))
        like_exist.liked = False
        like_exist.time_when_user_liked = datetime.utcnow()
        db.session.commit()
    else:
        # like doesn't exists
        new_like = Like(
                    liked=False,
                    time_when_user_liked=datetime.utcnow(),
                    user_id=current_user.id,
                    post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
    return jsonify({"message": "Unliked post"}), 201


@app.route('/api/analytics/')
@token_required
def analytics(current_user):
    date_from = datetime.strptime(request.args.get("date_from"), "%Y-%m-%d")
    date_to = datetime.strptime(request.args.get("date_to"), "%Y-%m-%d")
    my_query = (db.session.query(
                db.func.date_part('day', Like.time_when_user_liked)
                .label("day"),
                db.func.count(Like.liked))
                .filter(db.and_(Like.time_when_user_liked >= date_from,
                                Like.time_when_user_liked <= date_to,
                                Like.liked))
                .group_by("day").all())
    # TODO: maybe cast days to int from float?
    return jsonify({"likes_per_day": my_query})
