from itertools import groupby

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
yaml_file = open('engine_api/tasks/models/model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
loaded_model.load_weights('engine_api/tasks/models/model.h5')


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
    analysis_request = AnalysisRequest.query.filter_by(id=analysis_request_id).first()
    if analysis_request.analysis_complete:
        AnalysisRequest.query.filter_by(id=analysis_request_id).update({'status': StatusEnum.READY})
        db.session.commit()


@celery_app.task()
def perform_twitter_analysis(analysis_request_id):
    """
    Analyzes all the Tweets for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Tweets for
    :return:
    """
    # get all Tweets
    tweets = TextTwitter.query.filter_by(analysis_request_id=analysis_request_id).all()
    if len(tweets) == 0:
        # if there are no Tweets, mark Twitter analysis complete and return
        AnalysisRequest.query.filter_by(id=analysis_request_id).update({'twitter_analysis_complete': True})
        db.session.commit()
        # check to see if all analysis has been completed
        check_analysis_complete(analysis_request_id)
        return

    # group the Tweets by their date
    def key_func(k):
        return k.get_date
    sorted_tweets = sorted(tweets, key=key_func) # sort Tweets to be used with itertools.groupby
    grouped_tweets = []
    grouped_days = []
    for k, v in groupby(sorted_tweets, key=lambda x: x.get_date):
        grouped_days.append(k)
        grouped_tweets.append(list(v))

    # do analysis for every day
    for i in range(len(grouped_days)):
        # get the text of the Tweets
        text_list = []
        for tweet in grouped_tweets[i]:
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

        # get the AnalysisResults for the day
        exists = AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).first() is not None
        if exists:
            AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).update(analysis_values)
            db.session.commit()
        else:
            AnalysisResults.create(analysis_request_id=analysis_request_id, result_day=grouped_days[i])
            AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).update(analysis_values)
            db.session.commit()

    # Set the 'twitter_analysis_complete' to True here
    AnalysisRequest.query.filter_by(id=analysis_request_id).update({'twitter_analysis_complete': True})
    db.session.commit()

    # Then check to see if all analysis has been complete here
    check_analysis_complete(analysis_request_id)


@celery_app.task()
def perform_reddit_analysis(analysis_request_id):
    """
    Analyzes all the Reddit posts for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Reddit posts for
    :return:
    """
    # get all Reddit posts
    posts = TextReddit.query.filter_by(analysis_request_id=analysis_request_id).all()
    if len(posts) == 0:
        # if there are no Reddit posts, mark Reddit analysis complete and return
        AnalysisRequest.query.filter_by(id=analysis_request_id).update({'reddit_analysis_complete': True})
        db.session.commit()
        # check to see if all analysis has been completed
        check_analysis_complete(analysis_request_id)
        return

    # group the Reddit posts by their date
    def key_func(k):
        return k.get_date
    sorted_posts = sorted(posts, key=key_func) # sort Reddit posts to be used with itertools.groupby
    grouped_posts = []
    grouped_days = []
    for k, v in groupby(sorted_posts, key=lambda x: x.get_date):
        grouped_days.append(k)
        grouped_posts.append(list(v))

    # do analysis for every day
    for i in range(len(grouped_days)):
        # get the text of the Reddit posts
        text_list = []
        for post in grouped_posts[i]:
            text_list.append(post.serialize['text'])

        # reshape input text and classify Reddit post
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

        # get the AnalysisResults for the day
        exists = AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).first() is not None
        if exists:
            AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).update(analysis_values)
            db.session.commit()
        else:
            AnalysisResults.create(analysis_request_id=analysis_request_id, result_day=grouped_days[i])
            AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).update(analysis_values)
            db.session.commit()

    # Set the 'reddit_analysis_complete' to True here
    AnalysisRequest.query.filter_by(id=analysis_request_id).update({'reddit_analysis_complete': True})
    db.session.commit()

    # Then check to see if all analysis has been complete here
    check_analysis_complete(analysis_request_id)


@celery_app.task()
def perform_tumblr_analysis(analysis_request_id):
    """
    Analyzes all the Tumblr posts for an Analysis Request
    :param analysis_request_id: Analysis Request to perform the analysis of Tumblr posts for
    :return:
    """
    # get all Tumblr posts
    posts = TextTumblr.query.filter_by(analysis_request_id=analysis_request_id).all()
    if len(posts) == 0:
        # if there are no Tumblr posts, mark Tumblr analysis complete and return
        AnalysisRequest.query.filter_by(id=analysis_request_id).update({'tumblr_analysis_complete': True})
        db.session.commit()
        # check to see if all analysis has been completed
        check_analysis_complete(analysis_request_id)
        return

    # group the Tumblr posts by their date
    def key_func(k):
        return k.get_date
    sorted_posts = sorted(posts, key=key_func) # sort Tumblr posts to be used with itertools.groupby
    grouped_posts = []
    grouped_days = []
    for k, v in groupby(sorted_posts, key=lambda x: x.get_date):
        grouped_days.append(k)
        grouped_posts.append(list(v))

    # do analysis for every day
    for i in range(len(grouped_days)):
        # get the text of the Tumblr posts
        text_list = []
        for post in grouped_posts[i]:
            text_list.append(post.serialize['text'])

        # reshape input text and classify Tumblr post
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

        # get the AnalysisResults for the day
        exists = AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).first() is not None
        if exists:
            AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).update(analysis_values)
            db.session.commit()
        else:
            AnalysisResults.create(analysis_request_id=analysis_request_id, result_day=grouped_days[i])
            AnalysisResults.query.filter_by(analysis_request_id=analysis_request_id, result_day=grouped_days[i]).update(analysis_values)
            db.session.commit()

    # Set the 'reddit_analysis_complete' to True here
    AnalysisRequest.query.filter_by(id=analysis_request_id).update({'tumblr_analysis_complete': True})
    db.session.commit()

    # Then check to see if all analysis has been complete here
    check_analysis_complete(analysis_request_id)
