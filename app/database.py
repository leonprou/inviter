from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin

db = SQLAlchemy()

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False
    )
    user = db.relationship('User', back_populates='invitation')
    name = db.Column(db.String(160), nullable=False, unique=True)
    number_of_guests = db.Column(db.Integer, default=0)
    max_number_of_guests = db.Column(db.Integer, default=2)
    related_to = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80))

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    invitation = db.relationship("Invitation", uselist=False, back_populates="user")
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
