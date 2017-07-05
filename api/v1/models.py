from datetime import datetime

from flask_jwt_extended import get_jwt_identity
from passlib.apps import custom_app_context as pwdc
from headers import databases as db


class Eloquent():
    def __init__(self):
        pass

    # WRITING THE DATABASE
    # Commit values to the database
    def store(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    # Modifies a number of fields
    def put(self, payload):
        if payload:
            try:
                for attrb in payload.keys():
                    setattr(self, attrb, payload[attrb])
                db.session.commit()
                return True
            except:
                return False
        else:
            return False

    # Deletes the current record and store changes
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # READING THE DATABASE
    @classmethod
    def all(cls, lmt=0, q=None, uid=0):
        qword = '%{0}%'.format(q)
        if uid != 0:
            if q:
                return cls.query.filter(cls.name.ilike(qword)).filter(cls.user_id == uid).limit(lmt).all()
            else:
                return cls.query.filter(cls.user_id == uid).limit(lmt).all()
        else:
            if q:
                return cls.query.filter(cls.name.ilike(qword)).limit(lmt).all()
            else:
                return cls.query.limit(lmt).all()

    @classmethod
    def first(cls):
        return cls.query.first()

    @classmethod
    def find(cls, rid, uid=0):
        try:
            if uid != 0:
                record = cls.query.filter(cls.id == rid).filter(cls.user_id == uid).first()
            else:
                record = cls.query.filter(cls.id == rid).first()
            return record
        except:
            return None

    @classmethod
    def where(cls, **kwargs):
        return cls.query.filter_by(**kwargs)


class User(db.Model, Eloquent):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=True)
    buckets = db.relationship('Bucket', cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, payload=None):
        if payload:
            for attrb in payload.keys():
                setattr(self, attrb, payload[attrb])

        if "password" in payload.keys():
            self.hash_password(payload["password"])

    def hash_password(self, password):
        self.password = pwdc.hash(password)

    def verify_password(self, password):
        return pwdc.verify(password, self.password)

    @classmethod
    def login(cls, uname="", pword=""):
        try:
            user = User.where(username=uname).first()
            if pwdc.verify(pword, user.password):
                return user
            return False
        except:
            return False

class Bucket(db.Model, Eloquent):
    __tablename__ = 'bucket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, payload=None, uid=0):
        if payload:
            for attrb in payload.keys():
                setattr(self, attrb, payload[attrb])
            self.user_id = uid
2

class Item(db.Model, Eloquent):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, payload=None):
        if payload:
            for attrb in payload.keys():
                setattr(self, attrb, payload[attrb])
