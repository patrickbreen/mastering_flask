from flask import Flask, redirect, url_for

from webapp.config import DevConfig
from webapp.models import db
from webapp.controllers.main import main_blueprint
from webapp.controllers.blog import blog_blueprint
from webapp.extensions import bcrypt

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    return app

app = create_app(DevConfig)
app.register_blueprint(main_blueprint)
app.register_blueprint(blog_blueprint)

if __name__ == '__main__':
    app.run()
