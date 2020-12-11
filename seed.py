"""Seed file to make sample data for blogly db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# Post.query.delete()
User.query.delete()
Tag.query.delete()
PostTag.query.delete()

user1 = User(first_name="Alan", last_name="Tseng")
user2 = User(first_name="Sean", last_name="Kim")

db.session.add(user1)
db.session.add(user2)
db.session.commit()

post1 = Post(title="Alan's first post", content="Hello world!!!", user_id=user1.id)
post2 = Post(title="Alan's second post", content="blah blah blah", user_id=user1.id )
post3 = Post(title="Sean's first post", content="Good night world!!!", user_id=user2.id)
post4 = Post(title="Sean's second post", content="boo boo boo", user_id=user2.id)

tag1 = Tag(name="art")
tag2 = Tag(name="games")
tag3 = Tag(name="sports")
tag4 = Tag(name="food")


#add users, posts, tags to sesh

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)

db.session.commit()

post1.tags.append(tag1)
post1.tags.append(tag2)
post2.tags.append(tag3)
post2.tags.append(tag4)

#commit
db.session.commit()