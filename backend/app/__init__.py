from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os
from config.config import config

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version=app.config['API_VERSION'],
        title=app.config['API_TITLE'],
        description=app.config['API_DESCRIPTION'],
        prefix='/api',
        doc='/docs/'  # Swagger documentation at /docs/
    )
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(app.root_path, '..', app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    
    # Register namespaces/routes
    from app.api.songs import api as songs_api
    from app.api.upload import api as upload_api
    from app.api.health import api as health_api
    
    api.add_namespace(songs_api, path='/songs')
    api.add_namespace(upload_api, path='/upload')
    api.add_namespace(health_api, path='/health')
    
    return app

