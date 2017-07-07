import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy_utils.functions import drop_database

from api.v1.headers import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)


@manager.command
def dropdb():
    drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

manager.run()
