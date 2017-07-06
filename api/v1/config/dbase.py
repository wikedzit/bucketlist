default = "sqlite"


def db(current=None):
    if current is None:
        current = "postgress"
    dbase = {
        "sqlite":{
            'test': 'sqlite:///bktest.db',
            'develop': 'sqlite:///bkdevelop.db',
            'production': 'sqlite:///bkproduction.db'
        },

        "postgres": {
            'test': 'postgresql://@127.0.0.1/bktest',
            'develop': 'postgresql://@127.0.0.1/bkdevelop',
            'production': 'postgresql://@127.0.0.1/bkproduction'
        }
    }

    return dbase[current]

db_config = db()