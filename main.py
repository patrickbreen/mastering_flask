from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )


class Post(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(255))
  text = db.Column(db.Text())
  publish_date = db.Column(db.DateTime())
  comments = db.relationship(
      'Comment',
      backref='post',
      lazy='dynamic'
  )
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  tags = db.relationship(
      'Tag',
      backref='post',
      lazy='dynamic'
  )


class Tag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))


class Comment(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(255))
  text = db.Column(db.Text())
  date = db.Column(db.DateTime())
  post_id = db.Column(db.Integer(),
      db.ForeignKey('post.id'))


@app.route('/')
def home():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run()
