"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

NO_USER_IMG_URL = "https://p16-va.tiktokcdn.com/img/musically-maliva-obj/1662917669574661~c5_720x720.jpeg"


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
    image_url = db.Column(db.Text, default=NO_USER_IMG_URL)

    posts = db.relationship("Post", cascade="all, delete")

    def __repr__(self):
        """ Show info about user """
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @property
    def full_name(self):
        """ Return the user's full name """

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ Blog Post model """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User")
