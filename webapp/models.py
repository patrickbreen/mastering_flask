from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import AnonymousUserMixin

from webapp.extensions import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password,
                password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return unicode(self.id)


# make intermediate join table
tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
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
      secondary=tags,
      backref=db.backref('posts', lazy='dynamic')
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

class Reminder(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  date = db.Column(db.DateTime())
  email = db.Column(db.String())
  text = db.Column(db.Text())

  def __repr__(self):
      return "<Reminder '{}'>".format(self.text[:20])

