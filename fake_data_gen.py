import random
import datetime

from webapp.models import db, User, Post, Tag, Comment
from webapp import app

ctx = app.app_context()
ctx.push()

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
ctx.pop()
