from engine_api import celery
from engine_api.app import create_app, init_celery

app = create_app()
init_celery(app, celery)
