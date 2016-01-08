from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import AnonymousUserMixin

from webapp.extensions import bcrypt

db = SQLAlchemy()

# User <-> Roles join_table
roles = db.Table(
        'role_users',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
        )

# User Roles
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # relationships:
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    roles = db.relationship(
            'Role',
            secondary=roles,
            backref=db.backref('users', lazy='dynamic')
            )

    def __init__(self, username):
        self.username = username

        default = Role.query.filter_by(name="default").one()
        self.roles.append(default)

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
        return str(self.id)

# make intermediate join table for Tags <-> Posts
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


