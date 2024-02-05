from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))  # Store the url of the uploaded image
    filename = db.Column(db.String(255))  # Store the filename of the uploaded image
    link = db.Column(db.String(255))
    mean_value = db.Column(db.Float)  # Store the median value associated with the image
    title = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    api_key = db.Column(db.String(150))
    images = db.relationship('Image')  # Add a relationship to the Image model
    total = db.Column(db.Float, default=0.0)
    api_key_uses = db.Column(db.Integer, default=5, nullable=False)