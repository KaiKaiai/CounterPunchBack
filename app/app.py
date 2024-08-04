from flask import Flask
from flask_cors import CORS
from config import Config, basedir
from extensions import db
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'matches.db')
    CORS(app, resources={"*": {"origins": "*"}})
    
    db.init_app(app)
    
    ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
    if not ROBOFLOW_API_KEY:
        raise RuntimeError("ROBOFLOW_API_KEY environment variable is not set.")
    
    from roboflow import Roboflow
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project("boxing-lelg6")
    model = project.version(3).model
    
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
