# -*- coding: utf-8 -*-
"""Sentiment Analysis Engine endpoints"""
from flask import Blueprint

# import models for Flask-Migrate
from engine_api.engine.models import AnalysisRequest
from engine_api.engine.models import TextTwitter


blueprint = Blueprint('engine', __name__, url_prefix='/engine')


@blueprint.route('/test', methods=['GET'])
def test():
    return 'It works!'


@blueprint.route('/create')
def create():
    AnalysisRequest.create(
        keywords='coleman,cole,man'
    )

    return 'Complete!'


@blueprint.route('/create-tweet')
def create_tweet():
    TextTwitter.create(
        analysis_request_id=1
    )

    return 'Complete!'
