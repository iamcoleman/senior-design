# Celery import
from engine_api import celery as celery_app

# Database and Models (SQL Alchemy)
from engine_api.database import db
from engine_api.engine.models import AnalysisRequest, AnalysisResults
from engine_api.engine.models import TextTwitter, TextReddit, TextTumblr
from engine_api.engine.models import StatusEnum

# analysis imports
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
from keras.models import model_from_yaml


# Set memory growth in Tensorflow
# TODO: This is for Coleman's computer when using the GPU with Tensorflow,
#       I'm not sure how this will work on Jeet or Tim's computer
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# load the embed model
embed = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual/3')

# load the custom neural network
yaml_file = open('D:/_projects/senior-design/code/engine_api/engine_api/tasks/models/model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
loaded_model.load_weights('D:/_projects/senior-design/code/engine_api/engine_api/tasks/models/model.h5')


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


def check_analysis_complete(analysis_request_id):
    """
    Checks to see if all three texts have been analyzed, and if so it will update the Analysis Request status to READY
    :param analysis_request_id: Analysis Request to check on
    :return:
    """
    analysis_results = AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).first()
    if analysis_results.analysis_complete:
        AnalysisRequest.query.filter_by(id=analysis_request_id).update({'status': StatusEnum.READY})
        db.session.commit()


@celery_app.task()
def perform_twitter_analysis(analysis_request_id):
    """
    Analyzes all the Tweets for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Tweets for
    :return:
    """
    # get the text for all Tweets
    tweets = TextTwitter.query.filter_by(analysis_request_id=analysis_request_id).all()
    text_list = []
    for tweet in tweets:
        text_list.append(tweet.serialize['text'])

    # reshape input text and classify tweet
    positive_values = []
    for text in text_list:
        tweet_emb = np.array([tf.reshape(embed(text), [-1]).numpy()])
        y_pred = loaded_model.predict(tweet_emb)
        positive_value = y_pred[0][1]
        positive_values.append(positive_value)

    # get the result values
    median = np.median(positive_values)
    average = np.average(positive_values)
    upper_quartile = np.percentile(positive_values, 75)
    lower_quartile = np.percentile(positive_values, 25)
    min_value = min(positive_values)
    max_value = max(positive_values)
    analysis_values = {
        'twitter_median': median.item(),
        'twitter_average': average.item(),
        'twitter_lower_quartile': lower_quartile.item(),
        'twitter_upper_quartile': upper_quartile.item(),
        'twitter_minimum': min_value.item(),
        'twitter_maximum': max_value.item()
    }

    # update values in AnalysisResults table
    AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).update(analysis_values)
    AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).update({'twitter_analysis_complete': True})
    db.session.commit()

    # set all Tweets to analyzed
    TextTwitter.query.filter_by(analysis_request_id=analysis_request_id).update({'is_analyzed': True})
    db.session.commit()

    # check to see if all analysis has been completed
    check_analysis_complete(analysis_request_id)


@celery_app.task()
def perform_reddit_analysis(analysis_request_id):
    """
    Analyzes all the Reddit posts for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Reddit posts for
    :return:
    """
    # get the text for all Reddit posts
    posts = TextReddit.query.filter_by(analysis_request_id=analysis_request_id).all()
    text_list = []
    for post in posts:
        text_list.append(post.serialize['text'])

    # reshape input text and classify post
    positive_values = []
    for text in text_list:
        post_emb = np.array([tf.reshape(embed(text), [-1]).numpy()])
        y_pred = loaded_model.predict(post_emb)
        positive_value = y_pred[0][1]
        positive_values.append(positive_value)

    # get the result values
    median = np.median(positive_values)
    average = np.average(positive_values)
    upper_quartile = np.percentile(positive_values, 75)
    lower_quartile = np.percentile(positive_values, 25)
    min_value = min(positive_values)
    max_value = max(positive_values)
    analysis_values = {
        'reddit_median': median.item(),
        'reddit_average': average.item(),
        'reddit_lower_quartile': lower_quartile.item(),
        'reddit_upper_quartile': upper_quartile.item(),
        'reddit_minimum': min_value.item(),
        'reddit_maximum': max_value.item()
    }

    # update values in AnalysisResults table
    AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).update(analysis_values)
    AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).update({'reddit_analysis_complete': True})
    db.session.commit()

    # set all Reddit posts to analyzed
    TextReddit.query.filter_by(analysis_request_id=analysis_request_id).update({'is_analyzed': True})
    db.session.commit()

    # check to see if all analysis has been completed
    check_analysis_complete(analysis_request_id)


@celery_app.task()
def perform_tumblr_analysis(analysis_request_id):
    """
    Analyzes all the Tumblr posts for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Tumblr posts for
    :return:
    """
    # get the text for all Tumblr posts
    posts = TextTumblr.query.filter_by(analysis_request_id=analysis_request_id).all()
    text_list = []
    for post in posts:
        text_list.append(post.serialize['text'])

    # reshape input text and classify post
    positive_values = []
    for text in text_list:
        post_emb = np.array([tf.reshape(embed(text), [-1]).numpy()])
        y_pred = loaded_model.predict(post_emb)
        positive_value = y_pred[0][1]
        positive_values.append(positive_value)

    # get the result values
    median = np.median(positive_values)
    average = np.average(positive_values)
    upper_quartile = np.percentile(positive_values, 75)
    lower_quartile = np.percentile(positive_values, 25)
    min_value = min(positive_values)
    max_value = max(positive_values)
    analysis_values = {
        'tumblr_median': median.item(),
        'tumblr_average': average.item(),
        'tumblr_lower_quartile': lower_quartile.item(),
        'tumblr_upper_quartile': upper_quartile.item(),
        'tumblr_minimum': min_value.item(),
        'tumblr_maximum': max_value.item()
    }

    # update values in AnalysisResults table
    AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).update(analysis_values)
    AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id).update({'tumblr_analysis_complete': True})
    db.session.commit()

    # set all Tumblr posts to analyzed
    TextTumblr.query.filter_by(analysis_request_id=analysis_request_id).update({'is_analyzed': True})
    db.session.commit()

    # check to see if all analysis has been completed
    check_analysis_complete(analysis_request_id)
