from time import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
import jwt
from mobilXpertenApp import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)        

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
            
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
        }
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    price = db.Column(db.Integer,  index=True, unique=False)
    estimated_time = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, index=True, unique=False, default=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id')) # links instance of Repair to instance of Device

    def from_dict(self, data, new_repair=False):
        for field in ['name', 'price', 'estimated_time']:
            if field in data:
                setattr(self, field, data[field])
        if new_repair:
            setattr(self, 'timestamp', datetime.utcnow)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'estimated_time': self.estimated_time,
            'timestamp': self.timestamp,
            'is_available': self.is_available,
            'device_id': self.device_id,
        }

    def __repr__(self):
        return '<Repair {} - {}>'.format(self.name, self.price)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(64), index=True, unique=False)
    model = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    repairs = db.relationship('Repair', backref='device', lazy='joined')

    def from_dict(self, data, new_device=False):
        for field in ['model', 'brand']:
            if field in data:
                setattr(self, field, data[field])
        if new_device:
            setattr(self, 'timestamp', datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'timestamp': self.timestamp,
            'repairs': [r.to_dict() for r in self.repairs]
        }

    def __repr__(self):
        return '<device {} - {}>'.format(self.brand, self.model)