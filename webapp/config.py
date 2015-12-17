from os import path

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

