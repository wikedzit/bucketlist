import os
from datetime import timedelta
from . dbase import db_config

class AppConfig(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_config['develop']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    #JWT_TOKEN_LOCATION  = ['headers', 'cookies']
    #JWT_COOKIE_SECURE = False
    #JWT_ACCESS_COOKIE_PATH = '/api/v1/bucketlists/'
    #JWT_COOKIE_CSRF_PROTECT = False

class Testing(AppConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_config['test']

class Develop(AppConfig):
    SQLALCHEMY_DATABASE_URI = db_config['develop']

class Production(AppConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = db_config['production']
    #JWT_COOKIE_SECURE = True
    #JWT_COOKIE_CSRF_PROTECT = True

app_config = {
    'Testing': Testing,
    'Develop': Develop,
    'Production': Production
}
