import datetime

class Config(object):
    SECRET_KEY = '8ec801dcb5bad7a0c61d3e3adbed8699'
    RECAPTCHA_PUBLIC_KEY = '6LdXOBMTAAAAAFNV2npOcwIUKoIi6dVZkptnm57I'
    RECAPTCHA_PRIVATE_KEY = '6LdXOBMTAAAAADKX-bdKXq2eddHyX98wBbW-D1EW'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    # Celery stuff
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"

    CELERYBEAT_SCHEDULE = {
            'weely_digest': {
                'task': 'webapp.tasks.digest',
                'schedule': crontab(day_of_week=6, hour='10'),
                'args': (["email1@some.com", "email2@some.com"],)
                },
            }



