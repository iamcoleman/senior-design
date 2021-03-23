# -*- coding: utf-8 -*-
"""Sentiment Analysis Engine endpoints"""
from flask import Blueprint, jsonify, make_response, request
from engine_api.database import db
from sqlalchemy.exc import SQLAlchemyError

# import models for Flask-Migrate
from engine_api.engine.models import AnalysisRequest, AnalysisResults
from engine_api.engine.models import TextTwitter, TextReddit, TextTumblr

# celery tasks
from engine_api.tasks.workers import make_file, get_analysis_by_id
from engine_api.tasks.workers import perform_twitter_analysis, perform_reddit_analysis, perform_tumblr_analysis
import os


blueprint = Blueprint('engine', __name__, url_prefix='/engine')


@blueprint.route('/test', methods=['GET'])
def test():
    return 'It works!'


@blueprint.route('/test2', methods=['POST'])
def test2():
    perform_twitter_analysis.delay(11)

    return 'Ok'


@blueprint.route('/test3', methods=['GET'])
def test3():
    analysis_results = AnalysisResults.query.filter_by(analysis_request_id=11)
    # analysis_results.update({'twitter_analysis_complete': False})
    analysis_results.update({'tumblr_analysis_complete': True, 'reddit_analysis_complete': True})
    db.session.commit()

    return 'Ok'


@blueprint.route('/celery/<string:fname>/<string:content>')
def test_celery(fname, content):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    make_file.delay(fpath, content)
    return f'Find your file @ <code>{fpath}</code>'


@blueprint.route('/celery/test-db')
def test_celery_db():
    get_analysis_by_id.delay(2)

    return make_response(jsonify(success=True), 200)


"""

ANALYSIS REQUEST ENDPOINTS

"""


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
          analysis_results_id:
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

    # create the Analysis Results for the Analysis Request
    analysis_results = AnalysisResults.create(analysis_request_id=analysis_request.id)

    # build the response
    response = {
        'analysis_request_id': analysis_request.id,
        'analysis_results_id': analysis_results.id,
    }

    return jsonify(response)


"""

TWEET ENDPOINTS

"""


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


@blueprint.route('/tweets/loading-complete', methods=['POST'])
def begin_tweet_analysis():
    """
    Node.js server tells the Engine API that all Tweets have been successfully loaded into the database, which begins the sentiment analysis for only the Tweets
    ---
    parameters:
      - name: body
        in: body
        description: Analysis Request ID
        schema:
          $ref: '#/definitions/LoadingCompleteBody'
        required: true
    definitions:
      LoadingCompleteBody:
        type: object
        properties:
          analysis_request_id:
            type: number
    responses:
      200:
        description: Confirmation that the sentiment analysis has begun on the Tweets for the specified Analysis Request
    """
    # get the JSON data from the request
    data = request.json

    # start the Twitter analysis Celery task
    perform_twitter_analysis.delay(data['analysis_request_id'])

    return make_response(jsonify(success=True), 200)


"""

REDDIT ENDPOINTS

"""


@blueprint.route('/reddit', methods=['POST'])
def post_reddit():
    """
    Send a batch of Reddit posts/comments to be attached to an Analysis Request
    ---
    parameters:
      - name: body
        in: body
        description: Array of Reddit posts/comments
        schema:
          $ref: '#/definitions/RedditPostBody'
        required: true
    definitions:
      RedditPostBody:
        type: object
        properties:
          analysis_request_id:
            type: number
          posts:
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
        description: Confirmation that the Reddit posts/comments were successfully loaded
    """
    # get the JSON data from the request
    data = request.json

    # TODO: add error handling for this function
    insert_reddit(data['analysis_request_id'], data['posts'])

    return make_response(jsonify(success=True), 200)


def insert_reddit(analysis_request_id, posts):
    """
    Inserts the Reddit posts/comments all at once with a connectionless execution

    :param analysis_request_id: ID of the analysis request to tie the Reddit posts to
    :param posts: list of posts
    :return: ResultProxy object - https://stackoverflow.com/questions/20743806/sqlalchemy-execute-return-resultproxy-as-tuple-not-dict/54753785
    """
    # add the 'analysis_request_id' to every post dict
    for post in posts:
        post.update({"analysis_request_id": analysis_request_id})

    # insert all the posts to the TextReddit table
    result = None
    try:
        result = db.engine.execute(TextReddit.__table__.insert(), posts)
        result.close()
    except SQLAlchemyError as e:
        print(e)
        print(type(e))

    return result


@blueprint.route('/reddit/loading-complete', methods=['POST'])
def begin_reddit_analysis():
    """
    Node.js server tells the Engine API that all Reddit posts/comments have been successfully loaded into the database, which begins the sentiment analysis for only the Reddit posts/comments
    ---
    parameters:
      - name: body
        in: body
        description: Analysis Request ID
        schema:
          $ref: '#/definitions/LoadingCompleteBody'
        required: true
    responses:
      200:
        description: Confirmation that the sentiment analysis has begun on the Reddit posts/comments for the specified Analysis Request
    """
    # get the JSON data from the request
    data = request.json

    # start the Reddit analysis Celery task
    perform_reddit_analysis.delay(data['analysis_request_id'])

    return make_response(jsonify(success=True), 200)


"""

TUMBLR ENDPOINTS

"""


@blueprint.route('/tumblr', methods=['POST'])
def post_tumblr():
    """
    Send a batch of Tumblr posts/comments to be attached to an Analysis Request
    ---
    parameters:
      - name: body
        in: body
        description: Array of Tumblr posts/comments
        schema:
          $ref: '#/definitions/TumblrPostBody'
        required: true
    definitions:
      TumblrPostBody:
        type: object
        properties:
          analysis_request_id:
            type: number
          posts:
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
        description: Confirmation that the Tumblr posts/comments were successfully loaded
    """
    # get the JSON data from the request
    data = request.json

    # TODO: add error handling for this function
    insert_tumblr(data['analysis_request_id'], data['posts'])

    return make_response(jsonify(success=True), 200)


def insert_tumblr(analysis_request_id, posts):
    """
    Inserts the Tumblr posts/comments all at once with a connectionless execution

    :param analysis_request_id: ID of the analysis request to tie the Tumblr posts to
    :param posts: list of posts
    :return: ResultProxy object - https://stackoverflow.com/questions/20743806/sqlalchemy-execute-return-resultproxy-as-tuple-not-dict/54753785
    """
    # add the 'analysis_request_id' to every post dict
    for post in posts:
        post.update({"analysis_request_id": analysis_request_id})

    # insert all the posts to the TextReddit table
    result = None
    try:
        result = db.engine.execute(TextTumblr.__table__.insert(), posts)
        result.close()
    except SQLAlchemyError as e:
        print(e)
        print(type(e))

    return result


@blueprint.route('/tumblr/loading-complete', methods=['POST'])
def begin_tumblr_analysis():
    """
    Node.js server tells the Engine API that all Tumblr posts/comments have been successfully loaded into the database, which begins the sentiment analysis for only the Tumblr posts/comments
    ---
    parameters:
      - name: body
        in: body
        description: Analysis Request ID
        schema:
          $ref: '#/definitions/LoadingCompleteBody'
        required: true
    responses:
      200:
        description: Confirmation that the sentiment analysis has begun on the Tumblr posts/comments for the specified Analysis Request
    """
    # get the JSON data from the request
    data = request.json

    # start the Tumblr analysis Celery task
    perform_tumblr_analysis.delay(data['analysis_request_id'])

    return make_response(jsonify(success=True), 200)


"""

ANALYSIS RESULTS ENDPOINTS

"""


@blueprint.route('/analysis-request/<analysis_request_id>/status', methods=['GET'])
def check_analysis_status(analysis_request_id):
    """
    Check the status of an Analysis Request
    ---
    parameters:
      - name: analysis_request_id
        in: path
        description: The ID of the Analysis Request to check status of
        required: true
        type: number
    definitions:
      AnalysisRequestStatusResponse:
        type: object
        properties:
          status:
            type: string
            enum: [CREATED, LOADING_DATA, ANALYZING, READY, FAILURE]
    responses:
      200:
        description: Status of the Analysis Request
        schema:
          $ref: '#/definitions/AnalysisRequestStatusResponse'
    """
    analysis_request = AnalysisRequest.query.filter_by(analysis_request_id=analysis_request_id).first()

    return make_response(jsonify(status=analysis_request.get_status), 200)


@blueprint.route('/analysis-request/<analysis_request_id>/results', methods=['GET'])
def get_results(analysis_request_id):
    """
    Get the results for an Analysis Request
    ---
    parameters:
      - name: analysis_request_id
        in: path
        description: The ID of the Analysis Request to get the results for
        required: true
        type: number
    definitions:
      AnalysisRequestResultsResponse:
        type: object
        properties:
          analysis_request_id:
            type: number
          id:
            type: number
          reddit_analysis_complete:
            type: boolean
          reddit_average:
            type: number
          reddit_lower_quartile:
            type: number
          reddit_maximum:
            type: number
          reddit_median:
            type: number
          reddit_minimum:
            type: number
          reddit_upper_quartile:
            type: number
          tumblr_analysis_complete:
            type: boolean
          tumblr_average:
            type: number
          tumblr_lower_quartile:
            type: number
          tumblr_maximum:
            type: number
          tumblr_median:
            type: number
          tumblr_minimum:
            type: number
          tumblr_upper_quartile:
            type: number
          twitter_analysis_complete:
            type: boolean
          twitter_average:
            type: number
          twitter_lower_quartile:
            type: number
          twitter_maximum:
            type: number
          twitter_median:
            type: number
          twitter_minimum:
            type: number
          twitter_upper_quartile:
            type: number
    responses:
      200:
        description: Results for the Analysis Request
        schema:
          $ref: '#/definitions/AnalysisRequestResultsResponse'
    """
    analysis_results = AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).first()

    return make_response(jsonify(analysis_results.serialize), 200)
