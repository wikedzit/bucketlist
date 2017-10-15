from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from .config import app_config


app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='BucketList API',
          description='A Bucket List is a list of things that one has not done but wishes to accomplish them',
          licence="MIT",
          )


def envi(current=None):
    app.config.from_object(app_config['Develop'])
    if current:
        app.config.from_object(app_config[current])

envi('Production')
databases = SQLAlchemy(app)
