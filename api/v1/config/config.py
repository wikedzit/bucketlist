import os
from datetime import datetime
from . dbase import db_config

class AppConfig(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_config['develop']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)

class Testing(AppConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_config['test']

class Develop(AppConfig):
    SQLALCHEMY_DATABASE_URI = db_config['develop']

class Production(AppConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_config['production']


app_config = {
    'Testing': Testing,
    'Develop': Develop,
    'Production': Production
}
