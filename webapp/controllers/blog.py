import datetime

from flask import render_template, redirect, url_for, request, Blueprint
from sqlalchemy import func
from flask.ext.login import login_required

from webapp.models import db, Post, Tag, Comment, User, Tag, tags
from webapp.forms import CommentForm, PostForm

blog_blueprint = Blueprint(
        'blog',
        __name__,
        template_folder='../templates/blog',
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

@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post()
        new_post.title = form.title.data
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.post', post_id=new_post.id))

    recent, top_tags = sidebar_data()
    return render_template('new.html',
            form=form,
            recent=recent,
            top_tags=top_tags)

@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('blog.post',
            post_id=post.id))

    recent, top_tags = sidebar_data()
    return render_template('edit.html',
            form=form,
            post=post,
            recent=recent,
            top_tags=top_tags)

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
            return redirect(url_for('post', post_id=post.id))

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

@blog_blueprint.route('/user/<string:username>')
@blog_blueprint.route('/user/<string:username>/<int:page>')
def user(username, page=1):
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
        top_tags=top_tags
    )


