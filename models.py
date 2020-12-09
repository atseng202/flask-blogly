"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
    # May need default image
    image_url = db.Column(db.Text)

    def __repr__(self):
        """ Show info about user """
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    @classmethod
    def add_user(cls, f_name, l_name):
        """ Adds a user to users table """

        new_user = User(first_name="Test", last_name="Name")
        db.session.add(new_user)
        db.session.commit()
        