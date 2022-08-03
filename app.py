"""Blogly application."""

from flask import Flask, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.get('/')
def load_root_page():
    """Redirect to list of users."""
    
    return redirect("/users")

@app.get('/users')
def render_main_page():
    """Show all users."""
    all_users = User.query.all()
    return render_template("/users.html", users = all_users)

@app.get('/users/new')
def render_new_users_page():
    """Show an add form for users"""

@app.post('/users/new')
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""

@app.get('/users/<int:user_id>')
def render_user_page(user_id):
    """Show information about the given user."""

@app.get('/users/<int:user_id>/edit')
def render_edit_user_page():
    """Show the edit page for a user."""

@app.post('/users/<int:user_id>/edit')
def process_edit_user ():
    """Process the edit form, returning the user to the /users page."""

@app.post('/users/<int:user_id>/delete')
def delete_user():
    """Delete the user."""
