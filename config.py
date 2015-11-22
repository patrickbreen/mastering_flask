

class Config(object):
    SECRET_KEY = '8ec801dcb5bad7a0c61d3e3adbed8699'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_ECHO = True
