from unittest import TestCase

from app import app, NO_USER_IMG_URL
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    """ Tests for views for Blogly users """

    def setUp(self):
        """Add sample user."""

        # delete table first
        Post.query.delete()
        User.query.delete()

        bruce = User(first_name="Bruce", last_name="Wayne", image_url=NO_USER_IMG_URL)
        captain = User(
            first_name="Captain", last_name="America", image_url=NO_USER_IMG_URL
        )

        db.session.add(bruce)
        db.session.add(captain)

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_redirect_to_users(self):
        """Tests that navigating to root path
        redirects to users path"""

        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)

    def test_show_all_users(self):
        """ Check that users page show up """

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn("Bruce Wayne", html)
            self.assertIn("Captain America", html)

    def test_process_user_form(self):
        """ Checks that the new user form is processed and redirects to the right places """

        with app.test_client() as client:
            # Successful

            resp = client.post(
                "/users/new",
                data={"first_name": "Wonder", "last_name": "Woman", "image_url": ""},
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)
            self.assertIn("Wonder Woman", html)

            # Failures
            resp = client.post(
                "/users/new",
                data={"first_name": "Tom", "last_name": "", "image_url": ""},
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)
            self.assertIn("Last Name cannot be empty!", html)

            resp = client.post(
                "/users/new",
                data={"first_name": "", "last_name": "", "image_url": ""},
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)
            self.assertIn("First Name cannot be empty!", html)
            self.assertIn("Last Name cannot be empty!", html)

    def test_show_new_user_form(self):
        """ Test that the user form is rendered """

        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)
            self.assertIn('<button type="submit">Add</button>', html)

    def test_process_new_post_form(self):
        """ Checks that the new post form is processed and redirects to the user's page """

        with app.test_client() as client:
            # Successful
            bruce = User.query.get(1)
            resp = client.post(
                f"/users/{bruce.id}/posts/new",
                data={"post_title": "I am", "post_content": "the Batman"},
                follow_redirects=True,
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>Posts</h2>", html)
            self.assertIn("I am", html)

            # Failures
            bruce = User.query.get(1)
            resp = client.post(
                f"/users/{bruce.id}/posts/new",
                data={"post_title": "", "post_content": "the Batman"},
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Add Post for Bruce Wayne</h1>", html)
            self.assertIn("Title cannot be empty!", html)
            
            bruce = User.query.get(1)
            resp = client.post(
                f"/users/{bruce.id}/posts/new",
                data={"post_title": "", "post_content": ""},
                follow_redirects=True,
            )

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Add Post for Bruce Wayne</h1>", html)
            self.assertIn("Title cannot be empty!", html)
            self.assertIn("Content cannot be empty!", html)
