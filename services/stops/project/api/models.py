from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from project import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class StopRatings(db.Model):
    __tablename__ = "stopratings"

    entity_number = db.Column(db.Integer, primary_key=True)
    stop_number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, entity_number, stop_number, user_id, rating):
        self.entity_number = entity_number
        self.stop_number = stop_number
        self.user_id = user_id
        self.rating = rating
