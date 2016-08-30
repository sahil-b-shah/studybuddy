from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug import generate_password_hash, check_password_hash
from app import db, app
import datetime
 
#Base = declarative_base()

#for many-to-many relationship
# association_table = Table('association', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.user_id')),
#     Column('class_id', Integer, ForeignKey('classes.class_id'))
# )

association_table = db.Table('association',
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('class_id', Integer, ForeignKey('classes.class_id'))
)

curr_classes_association = db.Table('association2',
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('class_id', Integer, ForeignKey('classes.class_id'))
)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(1))
    year = db.Column(db.String(4))
    major = db.Column(db.String(120))
    bio = db.Column(db.String(1000))
    classes = relationship("Class", secondary=association_table, backref="users")
    current_class=db.Column(db.String(80))
    current_assignment=db.Column(db.String(10))
    current_room = db.Column(db.String(10))
    pwdhash = db.Column(db.String(100))
    group_id = db.Column(db.Integer, ForeignKey('groups.group_id'))
    #current_classes = relationship("Class", secondary=curr_classes_association, backref="current_users")
    location = db.Column(db.String(40))



    def __init__(self, firstname, lastname, email, gender, year, major, bio, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.gender = gender
        self.year = year
        self.major = major
        self.bio = bio
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '<User: %r, %r, %r, %r, %r>' % (self.user_id, self.email, self.firstname, self.classes, self.bio)
    # python 3
    @property
    def serialize(self):
        classes = []
        for class_ in self.classes:
            classes.append(class_.class_name)

        # current_classes = []
        # for class_ in self.current_classes:
        #     current_classes.append(class_.class_name)

        return {
            'id' : self.user_id,
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'gender' : self.gender,
            'year' : self.year,
            'major' : self.major,
            'bio' : self.bio,
            'location' : self.location,
            'classes': classes,
            'current course' : self.current_room,
        }

class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(10), unique=True)

    def __init__(self, class_name):
        self.class_name = class_name

    def get_id(self):
        try:
            return unicode(self.class_id)  # python 2
        except NameError:
            return str(self.class_id)

    def __repr__(self):
        return '<Class %r>' % self.class_name
  #python 3

class Group(db.Model):
    __tablename__='groups'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = (db.String(80))
    users = relationship("User", backref="group")

    def __init__(self, group_name):
        self.group_name=group_name

    @property
    def serialize(self):
        return {
            'group name': self.group_name,
            'group id': self.group_id
        }

class Online(db.Model):
    __tablename__='online_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    last_active = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user = relationship("User")

    def __init__(self, user_id, ):
        self.user_id = user_id

    def __repr__(self):
        return '<Online User: %r, %r>' % (self.user_id, self.last_active)

    def is_active(self):
        if self.last_active:
            reference = datetime.datetime.utcnow() - datetime.timedelta(minutes=app.config['ONLINE_LAST_MINUTES'])
            print self.last_active, reference
            if self.last_active > reference:
                return True
            else:
                return False
        else:
            return False



