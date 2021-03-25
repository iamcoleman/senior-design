"""Main application package."""
from celery import Celery

# TODO: Get the Redis URI into a configuration file
redis_uri = 'redis://localhost:6379'
celery = Celery(__name__.split('.')[0], backend=redis_uri, broker=redis_uri)
