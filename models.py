from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

db = SQLAlchemy()

"""
class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    speciality = db.Column(db.String, nullable=False)# db.ForeignKey("flights.id"),
    password = db.Column(db.String, nullable=False)# db.ForeignKey("flights.id"),
    email = db.Column(db.String(120), unique=True, nullable=False)

"""
class Project():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    startdate=db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    chef=db.Column(db.String,db.ForeignKey("pesons.id"))
    workers=[]
    def add_worker(Person):
        workers.append(Person)
    def remove_worker(Person):
        workers.pop(Person)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
