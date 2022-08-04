"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://images.unsplash.com/photo-1570116908808-4eeb66d9bb1e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80'


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """creates a new user"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(
        db.String(50),
        nullable=False)
    last_name = db.Column(
        db.String(50),
        nullable=False)
    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
        nullable=False)


class Post(db.Model):
    """creates Post table"""

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    title = db.Column(
        db.String(100),
        nullable=False)
    content = db.Column(
        db.Text,
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')
