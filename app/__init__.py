from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend

app.config.from_object(Config)
db = SQLAlchemy(app)

from . import routes, models

with app.app_context():
    db.create_all()