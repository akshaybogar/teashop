from flask import Flask
import os
from teaapp.alchemy_db import db
from flask_restplus import Api

api = Api()
app = Flask(__name__)
app.secret_key = 'Akshay'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

from teaapp import routes
