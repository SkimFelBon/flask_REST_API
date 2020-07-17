# app.py
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash  # check_password_hash
from marshmallow import ValidationError
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


@app.errorhandler(400)
def error_bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(422)
def error_unprocessable_entity(e):
    return jsonify(error=str(e)), 422


@app.route('/users/<pk>')
def get_user_temp(pk):
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


@app.route('/login')
def login():
    """TODO: Logins user"""
    # use jwt(jws) how?
    # create jwt token, set exp to few seconds and test it
    return


@app.route('/post')
def post():
    """TODO: leave post"""
    return


@app.route('/logout')
def logout():
    """TODO: logout user"""
    # remove jwt?
    return
