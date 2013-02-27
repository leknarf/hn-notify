import time
import os

import twitter

import db

MINIMUM_NEW_SCORE = 10

def tweet(scores):
    api = twitter.Api(
        consumer_key=os.environ['twitter_consumer_key'],
        consumer_secret=os.environ['twitter_consumer_secret'],
        access_token_key=os.environ['twitter_access_token'],
        access_token_secret=os.environ['twitter_token_secret']
    )
    message = "It's a good time to post! The second-highest score on 'New' is {new} and the second-lowest score on the front page is {front}.".format(**scores)

    api.PostUpdate(message)

def _should_post(scores):
    """
    Defines whether it is currently a "good time" to post
    """
    if (
        # We obviously want the new score to exceed the front page score
        scores['new'] > scores['front'] + 1
        # setting a minimum prevents us from posting in the middle of the night when no one is using HN
        and scores['new'] >= MINIMUM_NEW_SCORE
    ):
        return True
    return False

def _posted_recently():
    """
    We don't want to re-post if we've done so in the last hour
    """
    if (time.time() - db.fetch_notification_time()) < 60*60:
        return True
    return False

def notify(scores):
    if _should_post(scores) and not _posted_recently():
        db.update_notification_time()
        tweet(scores)
