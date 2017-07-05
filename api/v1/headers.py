from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from config.config import app_config

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='BucketList',
          description='A simple Bucketlist API',
          licence="MIT"
          )

ns = api.namespace('api/v1', description='Bucketlist operations')


def envi(current=None):
    app.config.from_object(app_config['Develop'])
    if current:
        app.config.from_object(app_config[current])

envi()
databases = SQLAlchemy(app)
