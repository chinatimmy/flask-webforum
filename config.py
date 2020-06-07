'''
This file is for boilerplate start up code don't 
'''
import os
import hashlib
from time import strftime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQL_ALCH_URL = "SQLALCHEMY_DATABASE_URI"

app.config[SQL_ALCH_URL] = "sqlite:///" + os.path.join(BASEDIR, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = "/uploads"
DB = SQLAlchemy(app)

# Limit how many posts are stored in the database
POST_LIMIT = 500