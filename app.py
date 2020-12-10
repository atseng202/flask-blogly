"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "SECRET!"
debug = DebugToolbarExtension(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

db.create_all()

NO_USER_IMG_URL = "https://p16-va.tiktokcdn.com/img/musically-maliva-obj/1662917669574661~c5_720x720.jpeg"


###### ROUTES FOR USERS ######

@app.route("/")
def redirect_to_users():
    """ Redirects to /users path """

    return redirect("/users")


@app.route("/users")
def show_all_users():
    """ Show all users of app """

    users = User.query.all()
    # .order_by('last_name').
    return render_template("users.html", users=users)


@app.route("/users/new")
def show_new_user_form():
    """ Show form to create a new user """

    return render_template("user-new.html")


@app.route("/users/new", methods=["POST"])
def process_new_user_form():
    """Get the new user form data and flash error messages
    if form input invalid or add the new user in the database
    """

    first_name = request.form["first_name"] or None
    last_name = request.form["last_name"] or None
    image_url = request.form["image_url"] or NO_USER_IMG_URL

    form_input_labels = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name')]

    if is_form_invalid(request.form, form_input_labels):
        return redirect("/users/new")

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_page(user_id):
    """ Shows the page of the user by the user ID """
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """ Shows the edit page for the user """

    user = User.query.get_or_404(user_id)
    return render_template("user-edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_user_form(user_id):
    """Get the edit user form data and flash error messages
    if form input invalid or update user data in the database
    """

    form_input_labels = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name')]

    if is_form_invalid(request.form, form_input_labels):
        return redirect(f"/users/{user_id}/edit")

    user = User.query.get(user_id)
    user.first_name = request.form["first_name"] or None
    user.last_name = request.form["last_name"] or None
    user.image_url = request.form["image_url"] or NO_USER_IMG_URL

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Get the user from user_id and delete from database """

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


def is_form_invalid(form_data, form_input_labels):
    """Checks the new user or edit user form data and
    makes sure that first_name and last_name are not empty.
    If there are invalid inputs, adds flash error messages
    and returns T/F.
    """

    invalid_ind = False

    for (key, label) in form_input_labels:
        if not form_data[key]:
            flash(f'{label} cannot be empty!')
            invalid_ind = True

    return invalid_ind

    # first_name = formData["first_name"] or None
    # last_name = formData["last_name"] or None

    # if not first_name:
    #     flash("First name cannot be empty!")

    # if not last_name:
    #     flash("Last name cannot be empty!")

    # return not first_name or not last_name


###### ROUTES FOR POSTS ######

@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """ Displays the page for adding a post """
    user = User.query.get_or_404(user_id)

    return render_template("post-new.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def process_new_post_form(user_id):
    """Get the new post form data and flash error messages
    if form input invalid or add the new post in the database
    """

    form_input_labels = [
        ('post_title', 'Title'),
        ('post_content', 'Content')]

    if is_form_invalid(request.form, form_input_labels):
        return redirect(f"/users/{user_id}/posts/new")

    user = User.query.get_or_404(user_id)

    new_post = Post(
        title=request.form['post_title'],
        content=request.form['post_content'],
        user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route("/posts/<int:post_id>")
def show_post_page(post_id):
    """ Shows the post page by the post ID """
    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """ Shows the page to edit a post by the post ID """
    post = Post.query.get_or_404(post_id)

    return render_template("post-edit.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_edit_post_form(post_id):
    """Get the edit post form data and flash error messages
    if form input invalid or edit the post in the database
    """

    form_input_labels = [
        ('post_title', 'Title'),
        ('post_content', 'Content')]

    if is_form_invalid(request.form, form_input_labels):
        return redirect(f"/posts/{post_id}/edit")

    post = Post.query.get_or_404(post_id)

    post.title = request.form["post_title"]
    post.content = request.form["post_content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')
