import datetime

from flask import Flask, render_template, redirect, \
                  url_for, request, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)

# the 'models':
class UserForm(Form):
  username = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
      )
  password = StringField(
      'Password',
      validators=[DataRequired(), Length(max=225)]
      )

class CommentForm(Form):
  name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
      )
  text = TextAreaField(u'Comment', validators=[DataRequired()])



class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

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


# the view/controller functions
blog_blueprint = Blueprint(
        'blog',
        __name__,
        template_folder='templates/blog',
        url_prefix='/blog'
        )

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
        ).join(
            tags
        ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags

@app.route('/')
def index():
    return redirect(url_for('blog.home'))


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_date.desc()
        ).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
     )

@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
@blog_blueprint.route('/post/<int:post_id>/<int:page>', methods=('GET', 'POST'))
def post(post_id, page=1):
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment()
            comment.name = form.name.data
            comment.text = form.text.data
            comment.post_id = post_id
            comment.date = datetime.datetime.now()

            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('post', post_id=post_id))

    post = Post.query.get_or_404(post_id)
    tags = post.tags

    comments = post.comments.order_by(Comment.date.desc()
        ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form
    )

@blog_blueprint.route('/tag/<string:tag_name>')
@blog_blueprint.route('/tag/<string:tag_name>/<int:page>')
def tag(tag_name, page=1):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()
        ).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )

@blog_blueprint.route('/user/<string:username>', methods=['GET', 'POST'])
@blog_blueprint.route('/user/<string:username>/<int:page>', methods=['GET', 'POST'])
def user(username, page=1):
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            user.username = form.username.data
            user.password = form.password.data

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user', username=user.username))

    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(
        Post.publish_date.desc()
        ).paginate(page, 10)

    recent, top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags=top_tags,
        form=form
    )


if __name__ == '__main__':
    app.register_blueprint(blog_blueprint)
    app.run(debug=True)
