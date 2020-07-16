# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)

from models import User, Post, Like


@app.route('/')
def index():
    """TODO: just a page with few posts"""
    # this page returns json, last 10 posts? or all posts?
    return


@app.route('/signup')
def signup():
    """TODO: allow registration for a user"""
    return


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
