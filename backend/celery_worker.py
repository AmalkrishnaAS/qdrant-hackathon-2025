import logging
from app import create_app
from app.extensions import celery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Create the app. This calls create_app, which configures the celery object
    app = create_app()
    
    # Push an application context to make it available for the tasks
    app.app_context().push()
    
    logger.info("Celery worker initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Celery worker: {e}")
    raise