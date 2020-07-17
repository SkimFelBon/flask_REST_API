# app.py
# RE.S.T. Representational State Transfer
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from authlib.jose import jwt
from datetime import datetime, timedelta
from functools import wraps
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)

from models import User  # , Post, Like
from schemas import UserSchema

user_schema = UserSchema()


@app.errorhandler(409)
def error_conflict(e):
    return jsonify(error=str(e)), 409


@app.errorhandler(401)
def error_unauthorized(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(400)
def error_bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(403)
def error_forbidden(e):
    return jsonify(error=str(e)), 403


@app.errorhandler(422)
def error_unprocessable_entity(e):
    return jsonify(error=str(e)), 422


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as error:
            app.logger.info(error)
            return jsonify({'message': 'Token is invalid'}), 401
        # TODO: also I need to check token expiretion date
        current_user = User.query.filter_by(id=data['sub']).first()
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/users/<pk>')
@token_required
def get_user_temp(current_user, pk):
    user = user_schema.dump(User.query.get(pk))
    app.logger.info(user)
    return jsonify({"user": user})


@app.route('/signup', methods=['POST'])
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
    app.logger.info(user_exist)
    if user_exist:
        return jsonify(
            abort(409, description="User with such email already exist"))
    hashed_pass = generate_password_hash(data['password'], method='sha256')
    new_user = User(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=hashed_pass)
    db.session.add(new_user)
    db.session.commit()
    user = user_schema.dump(User.query.get(new_user.id))
    return jsonify({'message': 'Created new User.', "user": user})


@app.route('/login', methods=['POST'])
def login():
    """TODO: Logins user"""
    json_data = request.get_json()
    app.logger.info(f"json_data: {json_data}")
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
    expire_at = datetime.utcnow() + timedelta(seconds=180)  # later use minutes
    payload = {'iss': 'Authlib', 'sub': user.id, 'exp': expire_at}
    signed_token = jwt.encode(header, payload, secret_key)
    # return to a user token
    return jsonify({"token": signed_token.decode('utf-8')})


@app.route('/post')
def post():
    """TODO: leave post"""
    return


@app.route('/logout')
def logout():
    """TODO: logout user"""
    # remove jwt?
    return

# when updating smth in db with PUT return 201 created
# DELETE returns 200 | or 404 not found
# POST returns 200
# GET returns 200
