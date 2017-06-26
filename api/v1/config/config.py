import os
from . dbase import db_config

class Testing(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_config['test']


class Develop(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_config['develop']


class Production(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = db_config['production']


app_config = {
    'Testing': Testing,
    'Develop': Develop,
    'Production': Production
}
