from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import Roboflow API key and initialize Roboflow client
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
if not ROBOFLOW_API_KEY:
    raise RuntimeError("ROBOFLOW_API_KEY environment variable is not set.")

from roboflow import Roboflow
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace().project("boxing-lelg6")
model = project.version(3).model

from app import routes, models

with app.app_context():
    db.create_all()
