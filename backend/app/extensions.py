from celery import Celery

# Instantiate the Celery object. It has no config yet.
celery = Celery(__name__)