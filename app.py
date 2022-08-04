"""Blogly application."""

from flask import Flask, redirect, render_template, request
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

@app.get('/users/')
def render_main_page():
    """Show all users."""
    all_users = User.query.all()
    return render_template("/users.html", users = all_users)

@app.get('/users/new/')
def render_new_users_page():
    """Show an add form for users"""
    return render_template('/new_user.html')

@app.post('/users/new/')
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""
    form_first_name = request.form['first-name']
    form_last_name = request.form['last-name']
    form_image_url = request.form['image-url']

    new_user = User(first_name = form_first_name
                    ,last_name = form_last_name,
                    image_url = form_image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users/')

@app.get('/users/<int:user_id>/')
def render_user_page(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('/user_details.html', user = user)

@app.get('/users/<int:user_id>/edit/')
def render_edit_user_page(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.post('/users/<int:user_id>/edit/')
def process_edit_user (user_id):
    """Process the edit form, returning the user to the /users page."""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']
    db.session.commit()

    return redirect (f'/users/{user_id}/')

@app.post('/users/<int:user_id>/delete/')
def delete_user(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()



    return redirect('/users')
