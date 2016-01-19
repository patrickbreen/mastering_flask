from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.restful import Api
from flask.ext.celery import Celery
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.cache import Cache


# rest API
rest_api = Api()

# bycrypt
bcrypt = Bcrypt()

# login manager
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
    from webapp.models import User
    return User.query.get(userid)


# Celery
celery = Celery()

# DebugToolbar
debug_toolbar = DebugToolbarExtension()

# Cache
cache = Cache()
