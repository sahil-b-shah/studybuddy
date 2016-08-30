from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os.path as op
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, ONLINE_LAST_MINUTES
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
#app.config.from_pyfile('../config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['ONLINE_LAST_MINUTES'] = ONLINE_LAST_MINUTES
app.secret_key = SECRET_KEY

CsrfProtect(app)


db = SQLAlchemy(app)
from models import Class, User, Group, Online

# Create Database if doesn't already exist
# if not op.isfile(app.config['SQLALCHEMY_DATABASE_NAME'][0]):
#   with app.app_context():
#     db.create_all()

if not op.isfile(app.config['SQLALCHEMY_DATABASE_URI']):
   with app.app_context():
   	print("creating new db in %s", app.config['SQLALCHEMY_DATABASE_URI'])
   	db.create_all()

import views
