from flask import Flask, redirect, url_for

from webapp.config import DevConfig
from webapp.models import db
from webapp.controllers.blog import blog_blueprint

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('blog.home'))

app.register_blueprint(blog_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
