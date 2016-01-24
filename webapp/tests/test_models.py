import unittest
import datetime

from webapp.models import (
        db,
        User,
        Post,
        Tag,
        Comment,
        Reminder
        )

from webapp import test_app

class TestUser(unittest.TestCase):

    username = "user1"
    password = "password"

    def setUp(self):
        db.app = test_app
        db.create_all()
        user = User()
        user.username = self.username
        user.set_password(self.password)
        db.session.add(user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password(self):
        user = User.query.filter(User.username == self.username).first()
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.check_password(self.password))


class TestPost(unittest.TestCase):

    # User
    username = "user1"
    password = "password"

    # Comment
    comment_name = "comment_name1"
    comment_text = "comment_text1"
    comment_date = datetime.datetime.now()

    # Tag
    tag_title = "tag_title1"

    # Post
    post_title = "post_title1"
    post_text = "post_text1"
    post_publish_date = datetime.datetime.now()

    def setUp(self):
        db.app = test_app
        db.create_all()
        user = User()
        user.username = self.username
        user.set_password(self.password)
        db.session.add(user)

        comment = Comment()
        comment.name = self.comment_name
        comment.text = self.comment_text

        tag = Tag()
        tag.title = self.tag_title

        post = Post()
        post.title = self.post_title
        post.text = self.post_text
        post.publish_date = self.post_publish_date

        # add relationships to other tables
        post.user = user
        post.tags = [tag]
        post.comments = [comment]

        db.session.add(user)
        db.session.add(comment)
        db.session.add(tag)
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_relationships(self):
        post = Post.query.first()

        self.assertEqual(post.user.username, self.username)
        self.assertEqual(post.title, self.post_title)
        self.assertEqual(post.tags[0].title, self.tag_title)
        self.assertEqual(post.comments[0].text, self.comment_text)



