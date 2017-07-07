default = "postgres"


def db(current=None):
    if current is None:
        current = "postgres"
    dbase = {
        "sqlite":{
            'test': 'sqlite:///bktest.db',
            'develop': 'sqlite:///bkdevelop.db',
            'production': 'sqlite:///bkproduction.db'
        },

        "postgres": {
            'test': 'postgresl://@127.0.0.1/bktest',
            'develop': 'postgresl://@127.0.0.1/bkdevelop',
            'production': 'postgresl://@127.0.0.1/bkproduction'
        }
    }

    return dbase[current]

db_config = db(default)