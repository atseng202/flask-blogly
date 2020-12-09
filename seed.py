"""Seed file to make sample data for blogly db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

user1 = User(first_name="Alan", last_name="Tseng")
user2 = User(first_name="Sean", last_name="Kim")

#add users to sesh
db.session.add(user1)
db.session.add(user2)

#commit
db.session.commit()