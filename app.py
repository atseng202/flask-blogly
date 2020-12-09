"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "SECRET!"
debug = DebugToolbarExtension(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

db.create_all()


@app.route("/")
def redirect_to_users():
    """ Redirects to /users path """

    return redirect("/users")


@app.route("/users")
def show_all_users():
    """ Show all users of app """

    users = User.query.all()
    return render_template("users.html", users=users)