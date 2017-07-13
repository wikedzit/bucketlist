default = "sqlite"


def db(current=None):
    if current is None:
        current = "postgres"
    dbase = {
        "sqlite":{
            'test': 'sqlite:///bktest',
            'develop': 'sqlite:///bkdevelop',
            'production': 'sqlite:///bkproduction'
        },

        "postgres": {
            'test': 'postgresql://@127.0.0.1:5432/bktest',
            'develop': 'postgresql://@127.0.0.1:5432/bkdevelop',
            'production': 'postgresql://@127.0.0.1:5432/bkproduction'
        }
    }

    return dbase[current]

db_config = db()