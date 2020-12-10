"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # TODO: Change to NOT NULL
    image_url = db.Column(db.Text)

    def __repr__(self):
        """ Show info about user """
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    @property
    def full_name(self):
        """ Return the user's full name """

        return f"{self.first_name} {self.last_name}"

    posts = db.relationship('Post')

    
class Post(db.Model):
    """ Blog Post model """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')
    
