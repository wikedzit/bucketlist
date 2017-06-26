from datetime import datetime
from passlib.apps import custom_app_context as pwdc
from ..imports import databases as db


class Eloquent():
    def __init__(self):
        pass

    # WRITING THE DATABASE
    # Commit values to the database
    def store(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

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
    def all(cls, lmt=0, q=None):
        qword = '%{0}%'.format(q)
        if q:
            if lmt > 0:
                return cls.query.limit(lmt).filter(cls.name.ilike(qword)).all()
            else:
                return cls.query.filter(cls.name.ilike(qword)).all()
        else:
            if lmt > 0:
                return cls.query.limit(lmt).all()
            else:
                return cls.query.all()

    @classmethod
    def first(cls):
        return cls.query.first()

    @classmethod
    def find(cls, rid):
        try:
            record = cls.query.get(rid)
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
        self.password = pwdc.encrypt(password)

    def verify_password(self, password):
        return pwdc.verify(password, self.password)

    @classmethod
    def login(cls, uname="", pword=""):
        user = User.where(username=uname).first()
        if pwdc.verify(pword, user.password):
            return user
        return False


class Bucket(db.Model, Eloquent):
    __tablename__ = 'bucket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, payload=None):
        if payload:
            for attrb in payload.keys():
                setattr(self, attrb, payload[attrb])
            user = User.first()
            self.user_id = user.id


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

