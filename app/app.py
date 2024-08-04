from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend
app.config.from_object(Config)

# Import Roboflow API key and initialize Roboflow client
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
if not ROBOFLOW_API_KEY:
    raise RuntimeError("ROBOFLOW_API_KEY environment variable is not set.")

from roboflow import Roboflow
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace().project("boxing-lelg6")
model = project.version(3).model

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
