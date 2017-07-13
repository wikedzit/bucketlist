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
            'postgres://rsfpvjsxfygkid:8a418489173dd41573bf7b762e6e8b8a9b6f2abcae0975e6579d79e944dc3369@ec2-54-225-242-74.compute-1.amazonaws.com:5432/d1ofcbjp9c27q3'
        }
    }

    return dbase[current]

db_config = db()