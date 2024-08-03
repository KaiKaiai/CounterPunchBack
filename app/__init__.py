from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://https://counter-punch.vercel.app/"}})

app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models

with app.app_context():
    db.create_all()
