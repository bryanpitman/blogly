"""Blogly application."""

from ast import Or
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, DEFAULT_IMAGE_URL
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
    return render_template("users.html", users = all_users)

@app.get('/users/new')
def render_new_users_page():
    """Show an add form for users"""
    return render_template('new_user.html')

@app.post('/users/new')
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""
    form_first_name = request.form['first-name']
    form_last_name = request.form['last-name']
    form_image_url = request.form['image-url'] or None


    new_user = User(first_name = form_first_name,
                    last_name = form_last_name,
                    image_url = form_image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect ('/users')

@app.get('/users/<int:user_id>')
def render_user_page(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    user_posts = user.posts
    return render_template('/user_details.html',
                            user = user,
                            user_posts = user_posts)

@app.get('/users/<int:user_id>/edit')
def render_edit_user_page(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.post('/users/<int:user_id>/edit')
def process_edit_user (user_id):
    """Process the edit form, returning the user to the /users page."""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']

    if request.form['image-url'] == '':
        user.image_url = DEFAULT_IMAGE_URL
    else:
        user.image_url = request.form['image-url']

    db.session.commit()

    return redirect (f'/users/{user_id}')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>/posts/new')
def render_new_post(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user = user)

@app.post('/users/<int:poster_id>/new_post')
def handle_new_post(poster_id):
    """Handle add form; add post and redirect to the user detail page.
    """
    user = User.query.get_or_404(poster_id)

    form_title = request.form['title']
    form_content = request.form['content']

    new_post = Post(title = form_title,
                    content = form_content,
                    user_id = poster_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{poster_id}')

