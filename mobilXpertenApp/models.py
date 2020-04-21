from time import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
import jwt
from mobilXpertenApp import db, login
from mobilXpertenApp.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

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

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return

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
            'password_hash': self.password_hash,
        }

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Repair(SearchableMixin, db.Model):
    __searchable__ = ['name', 'price']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    price = db.Column(db.Integer,  index=True, unique=False)
    estimated_time = db.Column(db.Integer, index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, index=True,
                             unique=False, default=True)
    # links instance of Repair to instance of SaleInfo
    sale_info_id = db.Column(
        db.Integer, db.ForeignKey('sale_info.id'), default=None)
    # links instance of Repair to instance of Device
    device_id = db.Column(db.Integer, db.ForeignKey('device_base.id'), default=None)

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


class DeviceBase(db.Model):
    __tablename__ = 'device_base'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(64), index=True, unique=False)
    img_url = db.Column(db.String(128), index=False, unique=False)
    typeOf = db.Column(db.String(128), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    __mapper_args__ = {
        'polymorphic_identity': 'device_base',
    }

    def from_dict(self, data, new_device=False):
        raise NotImplementedError('You need to define a from_dict() method!')

    def to_dict(self):
        raise NotImplementedError('You need to define a to_dict() method!')

    def __repr__(self):
        raise NotImplementedError('You need to define a __repr__() method!')


class RepairDevice(SearchableMixin, DeviceBase):
    __tablename__ = 'repair_device'
    __searchable__ = ['brand', 'model', 'typeOf']
    id = db.Column(db.Integer, db.ForeignKey('device_base.id'), primary_key=True)
    model = db.Column(db.String(64), index=True, unique=True)
    repairs = db.relationship('Repair', backref='device', lazy='joined')

    __mapper_args__ = {
        'polymorphic_identity':'repair_device',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'timestamp': self.timestamp,
            'img_url': self.img_url,
            'type': self.typeOf,
            'repairs': [r.to_dict() for r in self.repairs]
        }

    def from_dict(self):
        for field in ['model', 'brand', 'typeOf']:
            if field in data:
                setattr(self, field, data[field])
        if new_device:
            setattr(self, 'timestamp', datetime.utcnow)

    def __repr__(self):
        return '<RepairDevice {} - {} - {}>'.format(self.brand, self.model, self.typeOf)


class SaleDevice(SearchableMixin, DeviceBase):
    __tablename__ = 'sale_device'
    __searchable__ = ['brand', 'model', 'typeOf']
    id = db.Column(db.Integer, db.ForeignKey('device_base.id'), primary_key=True)
    model = db.Column(db.String(64), index=True, unique=False)
    
    sale_info = db.relationship("SaleInfo", uselist=False, back_populates="device")

    __mapper_args__ = {
        'polymorphic_identity':'sale_device',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'timestamp': self.timestamp,
            'img_url': self.img_url,
            'type': self.typeOf,
            'sale_info': self.sale_info.to_dict()
        }

    def from_dict(self):
        for field in ['model', 'brand', 'typeOf']:
            if field in data:
                setattr(self, field, data[field])
        if new_device:
            setattr(self, 'timestamp', datetime.utcnow)

    def __repr__(self):
        return '<SaleDevice {} - {} - {}>'.format(self.brand, self.model, self.typeOf)


class SaleInfo(db.Model):
    __tablename__ = 'sale_info'
    __searchable__ = ['grade', 'price_out', 'color', 'is_operator_locked', 'imei_number', 'memory_capacity']
    id = db.Column(db.Integer, primary_key=True)
    memory_capacity = db.Column(db.Integer,  index=True, unique=False)
    imei_number = db.Column(db.Integer,  index=True, unique=False)
    grade = db.Column(db.Integer, index=True, unique=False)  # 0: Perfect, 1: Minor imperfections, 2: OK, 3: Rough, 4: Barely Sellable
    color = db.Column(db.String(64), index=True, unique=False)
    price_in = db.Column(db.Integer,  index=True, unique=False)
    price_out = db.Column(db.Integer,  index=True, unique=False)
    is_operator_locked = db.Column(db.Boolean,  index=True, unique=False, default=False)
    operator_name = db.Column(db.String(64), index=False, unique=False, default=None)
    date_of_repair = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # creates a collection of Repairs objects
    # and creates a .sale_info on each Repair object which refers to the parent SaleInfo object
    repairs_done = db.relationship("Repair", backref="sale_info")
    
    
    device_id = db.Column(db.Integer, db.ForeignKey('device_base.id'))
    device = db.relationship("SaleDevice", uselist=False, back_populates="sale_info")

    def from_dict(self, data, new_saleInfo=False):
        for field in ['memory_capacity', 'imei_number', 'grade', 'color', 'price_out', 'is_operator_locked', 'operator_name', 'repairs_done']:
            if field in data:
                setattr(self, field, data[field])
        if new_saleInfo:
            setattr(self, 'date_of_repair', datetime.utcnow)

    def to_dict(self):
        return {
            'memory_capacity': self.memory_capacity,
            'imei_number': self.imei_number,
            'grade': self.grade,
            'color': self.color,
            'price_in': self.price_in,
            'price_out': self.price_out,
            'is_operator_locked': self.is_operator_locked,
            'operator_name': self.operator_name,
            'repairs_done': [r.to_dict() for r in self.repairs_done],
            'date_of_repair': self.date_of_repair,
            'device_id': self.device_id,
        }

    def __repr__(self):
        return '<SaleInfo {} - {} - {} - {} - {} SEK - {} SEK>'.format(self.imei_number, self.grade, self.color, self.price_in, self.price_out)
