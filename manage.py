from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy_utils.functions import drop_database
from api.v1.app import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)


@manager.command
def dropdb():
    drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == '__main__':
    manager.run()
