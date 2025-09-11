from app import create_app
from app.extensions import celery

# Create the app. This calls create_app, which configures the celery object
# that we imported from app.extensions
app = create_app()

# Push an application context to make it available for the tasks
app.app_context().push()