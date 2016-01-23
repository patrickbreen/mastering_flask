import unittest

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



