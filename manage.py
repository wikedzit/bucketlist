from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.imports import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)

if __name__ == '__main__':
    manager.run()
