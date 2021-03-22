# Celery import
from engine_api import celery as celery_app

# Database import
from engine_api.database import db

# Database Models
from engine_api.engine.models import AnalysisRequest


@celery_app.task()
def make_file(fname, content):
    with open(fname, 'w') as f:
        f.write(content)


@celery_app.task()
def get_analysis_by_id(analysis_request_id):
    analysis_request = AnalysisRequest.query.filter_by(id=analysis_request_id).all()
    print(analysis_request)
