from flask import Flask
from .v1.config.config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='BucketList API', description='A simple Bucketlist API')
ns = api.namespace('api/v1', description='Bucketlist operations')

def envi(current=None):
    app.config.from_object(app_config['Develop'])
    if current:
        app.config.from_object(app_config[current])


envi()
databases = SQLAlchemy(app)
