from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api.v1.headers import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)

if __name__ == '__main__':
    manager.run()
