from app.extensions import db

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, unique=True)
    number_of_guests = db.Column(db.Integer, default=0)
    max_number_of_guests = db.Column(db.Integer, default=2)
    related_to = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    email =db.Column(db.String(160), nullable=False, unique=True)
    status = db.Column(db.String(80))
