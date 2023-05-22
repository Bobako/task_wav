import configparser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
app.secret_key = config["SITE"]["secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = config["DATABASE"]["uri"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from app import models, routes

with app.app_context():
    db.create_all()