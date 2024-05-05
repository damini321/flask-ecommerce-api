from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


@app.route('/')
def welcome():
    return 'Welcome to the Flask application for managing products!'

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

from app import routes, models

# Initialize database
with app.app_context():
    db.create_all()

# Initialize JWTManager
jwt = JWTManager(app)