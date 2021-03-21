# -*- coding: utf-8 -*-
"""Sentiment Analysis Engine endpoints"""
from flask import Blueprint, jsonify, make_response, request
from engine_api.database import db
from sqlalchemy.exc import SQLAlchemyError

# import models for Flask-Migrate
from engine_api.engine.models import AnalysisRequest
from engine_api.engine.models import TextTwitter

# celery tasks
from engine_api.tasks.workers import make_file
import os


blueprint = Blueprint('engine', __name__, url_prefix='/engine')


@blueprint.route('/test', methods=['GET'])
def test():
    return 'It works!'


@blueprint.route('/celery/<string:fname>/<string:content>')
def test_celery(fname, content):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    make_file.delay(fpath, content)
    return f'Find your file @ <code>{fpath}</code>'


@blueprint.route('/analysis-request/<id>', methods=['GET'])
def get_analysis_request(id):
    """
    Get an existing Analysis Request Object
    ---
    parameters:
      - name: id
        in: path
        description: The ID of the Analysis Request to get
        required: true
        type: number
    definitions:
      AnalysisRequestGetResponse:
        type: object
        properties:
          id:
            type: number
          keywords:
            type: array
            items:
              type: string
          opened_at:
            type: string
          status:
            type: string
            enum: [CREATED, LOADING_DATA, ANALYZING, READY, FAILURE]
    responses:
      200:
        description: The Analysis Request object
        schema:
          $ref: '#/definitions/AnalysisRequestGetResponse'
    """
    # query on the analysis_request_id
    analysis_request = AnalysisRequest.query.get(id)

    return jsonify(analysis_request.serialize)


@blueprint.route('/analysis-request', methods=['POST'])
def create_analysis_request():
    """
    Create an Analysis Request Object
    ---
    parameters:
      - name: body
        in: body
        description: Array of keywords for the analysis
        schema:
          $ref: '#/definitions/AnalysisRequestCreationBody'
        required: true
    definitions:
      AnalysisRequestCreationBody:
        type: object
        properties:
          keywords:
            type: array
            items:
              type: string
      AnalysisRequestCreationResponse:
        type: object
        properties:
          analysis_request_id:
            type: number
    responses:
      200:
        description: The ID of the newly created Analysis Request
        schema:
          $ref: '#/definitions/AnalysisRequestCreationResponse'
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
    Send a batch of Tweets to be attached to an Analysis Request
    ---
    parameters:
      - name: body
        in: body
        description: Array of Tweets
        schema:
          $ref: '#/definitions/TweetPostBody'
        required: true
    definitions:
      TweetPostBody:
        type: object
        properties:
          analysis_request_id:
            type: number
          last_batch:
            type: boolean
          tweets:
            type: array
            items:
              type: object
              properties:
                created_at:
                  type: string
                text:
                  type: string
    responses:
      200:
        description: Confirmation that the tweets were successfully loaded
    """
    # get the JSON data from the request
    data = request.json

    # TODO: add error handling for this function
    insert_tweets(data['analysis_request_id'], data['tweets'])

    if data['last_batch']:
        print('last tweet batch received')
        begin_tweet_analysis()

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


@blueprint.route('/analysis-request/<analysis_request_id>/tweets', methods=['GET'])
def get_tweets(analysis_request_id):
    """
    Get Tweets attached to an Analysis Request
    Use '?analyzed=1' to return only the Tweets that have already been analyzed
    Use '?not-analyzed=1' to return only the Tweets that have not been analyzed
    Note: analyzed will take precedence over not-analyzed if both are set to 1
    ---
    parameters:
      - name: analysis_request_id
        in: path
        description: The ID of the Analysis Request to get Tweets for
        required: true
        type: number
      - name: analyzed
        in: query
        description: Boolean (0/1) to filter for only the Tweets that have been analyzed
        required: false
        type: number
      - name: not-analyzed
        in: query
        description: Boolean (0/1) to filter for only the Tweets that have not been analyzed
        required: false
        type: number
    definitions:
      AnalysisRequestTweetsResponse:
        type: array
        items:
          type: object
          properties:
            created_at:
              type: string
            text:
              type: string
    responses:
      200:
        description: Array of Tweets
        schema:
          $ref: '#/definitions/AnalysisRequestTweetsResponse'
    """
    filter_analyzed = int(request.args.get('analyzed', default=0))
    filter_not_analyzed = int(request.args.get('not-analyzed', default=0))

    # 'filter_analyzed' takes precedence over 'filter_not_analyzed' if both set to True
    tweets = None
    if filter_analyzed:
        # return analyzed tweets
        try:
            tweets = TextTwitter.query.filter_by(analysis_request_id=analysis_request_id, is_analyzed=True).all()
        except SQLAlchemyError as e:
            print(e)
            print(type(e))
    elif filter_not_analyzed:
        # return not analyzed tweets
        try:
            tweets = TextTwitter.query.filter_by(analysis_request_id=analysis_request_id, is_analyzed=False).all()
        except SQLAlchemyError as e:
            print(e)
            print(type(e))
    else:
        # return all tweets
        try:
            tweets = TextTwitter.query.filter_by(analysis_request_id=analysis_request_id).all()
        except SQLAlchemyError as e:
            print(e)
            print(type(e))

    response = {
        'tweets': [tweet.serialize for tweet in tweets]
    }

    return jsonify(response)


def begin_tweet_analysis():
    return
