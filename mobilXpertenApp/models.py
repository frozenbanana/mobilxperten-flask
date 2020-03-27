from time import time
from mobilXpertenApp import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    price = db.Column(db.Integer,  index=True, unique=False)
    estimated_time = db.Column(db.Integer,  index=True, unique=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def __repr__(self):
        return '<Repair {} - {}>'.format(self.name, self.price)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(64), index=True, unique=True)
    brand = db.Column(db.String(64), index=True, unique=False)
    repairs = db.relationship('Repair', backref='device', lazy='dynamic')

    def __repr__(self):
        return '<device {} - {}>'.format(self.brand, self.username)