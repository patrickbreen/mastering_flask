from flask import Flask, redirect, url_for
from flask.ext.restful import Api

from sqlalchemy import event

from webapp.config import DevConfig, TestConfig
from webapp.models import db, Reminder
from webapp.controllers.main import main_blueprint
from webapp.controllers.blog import blog_blueprint
from webapp.extensions import (
        bcrypt, login_manager, debug_toolbar, cache
        )
from webapp.controllers.rest.post import PostApi

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)

    rest_api = Api(app)
    rest_api.add_resource(PostApi,
            '/restapi/post',
            '/restapi/post/<int:post_id>',
            endpoint='restapi')

    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)
    return app

# make a dev app
dev_app = create_app(DevConfig)

# make a test app
test_app = create_app(TestConfig)
