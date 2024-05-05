from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


@app.route('/')
def welcome():
    return 'Welcome to the Flask application for managing products!'


from app import routes, models

# Initialize database
with app.app_context():
    db.create_all()
