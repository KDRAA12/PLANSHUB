from flask import Flask,render_template,jsonify,request,abort
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()

db1 = SQLAlchemy()

app=Flask(__name__)
if not os.getenv("db_uri"):
    raise RuntimeError("DATABASE URI NOT FOUND")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

engine = create_engine(os.getenv("db_uri"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/draw')
def drawing():
    return render_template("draw2.html")


@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        return jsonify({'error':'errd'})
    user = User(username = username)
    user.hash_password(password)
    verify_password(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}  


@app.route('/api/resource',methods=['GET'])
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

@app.route('/api/',methods=['GET'])
def get_api_resource():
    return jsonify({ 'data': 'Hello, !' })

@app.route('/login',methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is None:
        abort(400) # user do not exist
    if verify_password(username, password):
        db.session.add(user)
        db.session.commit()
    else:
        abort(400) # wrong password

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

class Project(db1.Model):
    __tablename__="projects"
    id = db1.Column(db1.Integer, primary_key=True)
    name = db1.Column(db1.String, nullable=False)
    startdate=db1.Column(db1.DateTime,default=datetime.utcnow, nullable=False)
    chef=db1.Column(db1.String,db1.ForeignKey("pesons.id"))
    workers=[]
    def add_worker(Person):
        workers.append(Person)
        db.session.commit()
    def remove_worker(Person):
        workers.pop(Person)
        db.session.commit()
class User(db1.Model):
    __tablename__ = 'users'
    id = db1.Column(db1.Integer, primary_key = True)
    username = db1.Column(db1.String(32), index = True)
    password_hash = db1.Column(db1.String(128))
    


if __name__=='__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5005)

