# config.py

import settings


class Config:
    DEVELOPMENT = False
    DEBUG = False
    SECRET_KEY = settings.SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3" # relative path
    SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
