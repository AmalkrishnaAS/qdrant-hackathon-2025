from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import os
from config.config import config
from .extensions import celery

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    celery.config_from_object(app.config, namespace='CELERY')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    # --- Celery is now configured ---

    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version=app.config['API_VERSION'],
        title=app.config['API_TITLE'],
        description=app.config['API_DESCRIPTION'],
        prefix='/api',
        doc='/docs/'
    )
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(app.root_path, '..', app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    
    # Register namespaces inside the factory
    from app.api.songs import api as songs_api
    from app.api.upload import api as upload_api
    from app.api.health import api as health_api
    from app.api.tasks import api as tasks_api
    
    api.add_namespace(songs_api, path='/songs')
    api.add_namespace(upload_api, path='/upload')
    api.add_namespace(health_api, path='/health')
    api.add_namespace(tasks_api, path='/tasks')
    
    # Try to register AI recommendations API if available
    try:
        from app.api.recommendations import api as recommendations_api
        api.add_namespace(recommendations_api, path='/recommendations')
    except ImportError as e:
        print(f"AI recommendations API not available: {e}")
    
    return app

# REMOVE THESE LINES FROM THE BOTTOM OF THE FILE
# app = create_app()
# celery = celery_utils.make_celery(app)