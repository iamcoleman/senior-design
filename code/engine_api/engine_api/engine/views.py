# -*- coding: utf-8 -*-
"""Sentiment Analysis Engine endpoints"""
from flask import Blueprint, jsonify, make_response, request
from engine_api.database import db
from sqlalchemy.exc import SQLAlchemyError

# import models for Flask-Migrate
from engine_api.engine.models import AnalysisRequest
from engine_api.engine.models import TextTwitter

blueprint = Blueprint('engine', __name__, url_prefix='/engine')


@blueprint.route('/test', methods=['GET'])
def test():
    return 'It works!'


@blueprint.route('/analysis-request', methods=['GET'])
def get_analysis_request():
    """
    :post_body: {
        "analysis_request_id": 1
    }
    :return:
    """
    # get the JSON data from the request
    data = request.json
    analysis_request_id = data['analysis_request_id']

    # query on the analysis_request_id
    analysis_request = AnalysisRequest.query.get(analysis_request_id)

    return jsonify(analysis_request.serialize)


@blueprint.route('/analysis-request', methods=['POST'])
def create_analysis_request():
    """
    :post_body: {
        "keywords": ["key", "words"]
    }
    :return:
    """
    # get the JSON data from the request
    data = request.json
    keywords = ','.join(data['keywords'])

    # create the Analysis Request
    analysis_request = AnalysisRequest.create(keywords=keywords)

    # build the response
    response = {
        'analysis_request_id': analysis_request.id
    }

    return jsonify(response)


@blueprint.route('/tweets', methods=['POST'])
def post_tweets():
    """
    :post_body: {
        "analysis_request_id": 1,
        "tweets": [
            <TweetObject>
        ]
    }
    :TweetObject: {
        "created_at": DateTime,
        "text": "text of the tweet"
    }
    :return:
    """
    # get the JSON data from the request
    data = request.json

    insert_tweets(data['analysis_request_id'], data['tweets'])

    return make_response(jsonify(success=True), 200)


def insert_tweets(analysis_request_id, tweets):
    """
    Inserts the Tweets all at once with a connectionless execution

    :param analysis_request_id: ID of the analysis request to tie the Tweets to
    :param tweets: list of tweets
    :return: ResultProxy object - https://stackoverflow.com/questions/20743806/sqlalchemy-execute-return-resultproxy-as-tuple-not-dict/54753785
    """
    # add the 'analysis_request_id' to every tweet dict
    for tweet in tweets:
        tweet.update({"analysis_request_id": analysis_request_id})

    # insert all the tweets to the TextTwitter table
    result = None
    try:
        result = db.engine.execute(TextTwitter.__table__.insert(), tweets)
        result.close()
    except SQLAlchemyError as e:
        print(e)
        print(type(e))

    return result


@blueprint.route('/tweets', methods=['GET'])
def get_tweets():
    """
    Gets Tweets (analyzed, not analyzed, or all) for a specific AnalysisRequest

    :post_body: {
        "analysis_request_id": 1,
        "filter_analyzed": Boolean,
        "filter_not_analyzed": Boolean
    }
    :return: list of serialized Tweets
    """
    data = request.json

    # 'filter_analyzed' takes precedence over 'filter_not_analyzed' if both set to True
    tweets = None
    if data['filter_analyzed']:
        # return analyzed tweets
        try:
            tweets = TextTwitter.query.filter_by(is_analyzed=True).all()
        except SQLAlchemyError as e:
            print(e)
            print(type(e))
    elif data['filter_not_analyzed']:
        # return not analyzed tweets
        try:
            tweets = TextTwitter.query.filter_by(is_analyzed=False).all()
        except SQLAlchemyError as e:
            print(e)
            print(type(e))
    else:
        # return all tweets
        try:
            tweets = TextTwitter.query.all()
        except SQLAlchemyError as e:
            print(e)
            print(type(e))

    response = {
        'tweets': [tweet.serialize for tweet in tweets]
    }

    return jsonify(response)

