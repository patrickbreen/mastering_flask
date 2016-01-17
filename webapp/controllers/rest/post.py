import datetime

from flask import abort
from flask.ext.restful import Resource, fields, marshal_with

from webapp.models import db, User, Post, Tag
from webapp.controllers.rest.parsers import (
        post_get_parser,
        post_post_parser,
        post_put_parser
        )

nested_tag_fields = {
        'id': fields.Integer(),
        'title': fields.String()
        }

post_fields = {
        'username': fields.String(),
        'title': fields.String(),
        'text': fields.String(),
        'tags': fields.List(fields.Nested(nested_tag_fields)),
        'publish_date': fields.DateTime(dt_format='iso8601')
        }

class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self, post_id=None):
        args = post_get_parser.parse_args()
        page = args['page'] or 1
        username = args['username']

        # A post id was supplied so simply return that single post
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)

            return post

        # If a username is supplied in the GET arguments, filter
        # posts by it
        elif username:
            user = User.query.filter_by(
                    username=username
                    ).first()

            if not user:
                abort(404)

            posts = user.posts.order_by(
                    Post.publish_date.desc()
                    ).paginate(page, 30)

        # Otherwise, just get all posts
        else:
            posts = Post.query.order_by(
                    Post.publish_date.desc()
                    ).paginate(page, 30)

        return posts.items

    def post(self, post_id=None):
        if post_id:
            abort(400)
        else:
            args = post_post_parser.parse_args(strict=True)
            username = args['username']
            password = args['password']
            user = User.query.filter_by(username=username).first()

            if not user:
                abort(401)

            if not user.check_password(password):
                abort(401)

            new_post = Post()
            new_post.user_id = user.id
            new_post.title = args['title']
            new_post.publish_date = datetime.datetime.now()
            new_post.text = args['text']

            if args['tags']:
                for t_title in args['tags']:
                    tag = Tag.query.filter_by(title=t_title).first()

                    # Add the tag if it exists. If not make a new tag.
                    if tag:
                        new_post.tags.append(tag)
                    else:
                        new_tag = Tag()
                        new_tag.title = t_title
                        new_post.tags.append(new_tag)

            db.session.add(new_post)
            db.session.commit()
            return new_post.id, 201

    def delete(self, post_id=None):
        if not post_id:
            abort(400)

        post = Post.query.get(post_id)
        if not post:
            abort(404)

        args = post_put_parser.parse_args(strict=True)
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            abort(401)
        if not user.check_password(args['password']):
            abort(401)
        if user != post.user:
            abort(403)

        db.session.delete(post)
        db.session.commit()
        return "", 204


