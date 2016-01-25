import random
import datetime

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean

from webapp import dev_app
from webapp.models import db,  User, Post, Tag, Comment, Reminder

db.init_app(dev_app)

manager = Manager(dev_app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    return dict(dev_app=dev_app, db=db,
        User=User, Post=Post, Tag=Tag, Comment=Comment,
        Reminder=Reminder,
        )

@manager.command
def init_db():
    "create and populate db with default dev data"
    populate_default_data(db, dev_app)

def populate_default_data(db, app):
    db.app = app
    db.create_all()

    user = User()
    user.username = 'jim'
    user.set_password('jim')
    db.session.add(user)
    db.session.commit()

    tag_one = Tag(title='Python')
    tag_two = Tag(title='Flask')
    tag_three = Tag(title='SQLAlchemy')
    tag_four = Tag(title='Jinja')
    tag_list = [tag_one, tag_two, tag_three, tag_four]
    s = "Example text"


    for i in range(100):
        new_post = Post(title="Post " + str(i))
        new_post.user = user
        new_post.publish_date = datetime.datetime.now()
        new_post.text = s
        new_post.tags = random.sample(tag_list, random.randint(1,3))
        db.session.add(new_post)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
