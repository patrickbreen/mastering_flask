from flask import (
        render_template, redirect,
        url_for, request, Blueprint, flash)
from sqlalchemy import func
from flask.ext.login import login_user, logout_user

from webapp.forms import LoginForm, RegisterForm
from webapp.models import User, Post, Tag, tags, db

main_blueprint = Blueprint(
        'main',
        __name__,
        template_folder='../templates/main')

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
        ).join(
            tags
        ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags

@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember.data)

    recent, top_tags = sidebar_data()
    return render_template('login.html',
            form=form,
            recent=recent,
            top_tags=top_tags)

@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created, please log in.',
                category='success')

        return redirect(url_for('main.login'))

    recent, top_tags = sidebar_data()
    return render_template('register.html',
            form=form,
            recent=recent,
            top_tags=top_tags)
