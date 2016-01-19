import random
import datetime

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean

from webapp import app
from webapp.models import db, User, Post, Tag, Comment, Reminder

db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db,
        User=User, Post=Post, Tag=Tag, Comment=Comment,
        Reminder=Reminder,
        )

@manager.command
def create_db():
    "create the database if it doesn't already exist"
    db.create_all()

@manager.command
def populate():
    "populate with default data"

    # populate roles
    db.session.add(Role('admin'))
    db.session.add(Role('poster'))
    db.session.add(Role('default'))
    db.session.commit()

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
