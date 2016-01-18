from flask import Flask, redirect, url_for

from sqlalchemy import event

from webapp.config import DevConfig
from webapp.models import db, Reminder
from webapp.controllers.main import main_blueprint
from webapp.controllers.blog import blog_blueprint
from webapp.extensions import bcrypt, login_manager, rest_api
from webapp.controllers.rest.post import PostApi
from webapp.tasks import on_reminder_save

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    event.listen(Reminder, 'after_insert', on_reminder_save)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)
    return app

# make a Dev app
app = create_app(DevConfig)
rest_api.add_resource(PostApi,
        '/api/post',
        '/api/post/<int:post_id>',
        endpoint='api')

rest_api.init_app(app)


if __name__ == '__main__':
    app.run()
