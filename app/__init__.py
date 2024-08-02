from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend

from app import routes
