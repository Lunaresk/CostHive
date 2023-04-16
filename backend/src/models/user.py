import jwt
from src import db, login
from flask import current_app
from flask_login import UserMixin
from marshmallow import Schema, fields
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    LoginToken = db.relationship("LoginToken", backref='User', lazy='dynamic')
    Bought = db.relationship("Bought", secondary="login_token",
        lazy='dynamic', overlaps="User,LoginToken")
    EstablishmentCandidate = db.relationship("EstablishmentCandidate", backref='User', lazy='dynamic')
    Establishment = db.relationship("Establishment", backref="User", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email})>"

class UserSchema(Schema):
    id = fields.Number()
    email = fields.Str()
    password_hash = fields.Str()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))