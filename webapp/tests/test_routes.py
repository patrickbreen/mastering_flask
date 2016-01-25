import unittest

import webapp.controllers.blog as blog
from webapp import test_app
from webapp.models import db
from manage import populate_default_data

db.init_app(test_app)

class BlogRoutesTestCase(unittest.TestCase):

    def setUp(self):
        populate_default_data(db, test_app)


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_example(self):
        self.assertTrue(True)

    # Routes:
    # '/', home
    # '/new' new_post (GET, POST)
    # '/edit/<int>' edit_post (GET, POST)
    #  '/post/<int>' post (GET, POST)
    # '/tag/<string>'
    # '/user/<int>


class MainRoutesTestCase(unittest.TestCase):

    def setUp(self):
        populate_default_data(db, test_app)


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_example(self):
        self.assertTrue(True)

    # Routes:
    # '/', home
    # '/login'
    # '/logout'
    # '/register'

