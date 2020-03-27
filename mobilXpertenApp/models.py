from mobilXpertenApp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


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