from extensions import db

class Opportunity(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    duration = db.Column(
        db.String(100),
        nullable=False
    )

    start_date = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    skills = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    future_opportunities = db.Column(
        db.Text,
        nullable=False
    )

    max_applicants = db.Column(
        db.Integer,
        nullable=True
    )

    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("admin.id"),
        nullable=False
    )