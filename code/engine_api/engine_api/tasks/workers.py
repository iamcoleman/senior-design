# Celery import
from engine_api import celery as celery_app

# Database and Models (SQL Alchemy)
from engine_api.database import db
from engine_api.engine.models import AnalysisRequest
from engine_api.engine.models import TextTwitter

# embed


@celery_app.task()
def make_file(fname, content):
    """Used for testing Celery"""
    with open(fname, 'w') as f:
        f.write(content)


@celery_app.task()
def get_analysis_by_id(analysis_request_id):
    """Used for testing Celery"""
    analysis_request = AnalysisRequest.query.filter_by(id=analysis_request_id).all()
    print(analysis_request)


@celery_app.task()
def perform_twitter_analysis(analysis_request_id):
    """
    Analyzes all the Tweets for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Tweets for
    :return:
    """
    tweets = TextTwitter.query.filter_by(analysis_request_id=analysis_request_id).all()
    pass
