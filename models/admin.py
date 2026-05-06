from flask_login import UserMixin

from extensions import db

from models.opportunity import Opportunity

class Admin(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    opportunities = db.relationship(
        "Opportunity",
        backref="admin",
        lazy=True,
        cascade="all, delete-orphan"
    )