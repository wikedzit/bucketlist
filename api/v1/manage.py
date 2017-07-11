from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy_utils.functions import create_database, drop_database

from headers import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)


@manager.command
def createdb():
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

@manager.command
def dropdb():
    drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    manager.run()
