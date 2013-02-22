import time
import os

import twitter

import db

def tweet(scores):
    api = twitter.Api(
        consumer_key=os.environ['twitter_consumer_key'],
        consumer_secret=os.environ['twitter_consumer_secret'],
        access_token_key=os.environ['twitter_access_token'],
        access_token_secret=os.environ['twitter_token_secret']
    )
    message = "It's a good time to post! The median high score on 'New' is {new} and the median low score on the front page is {front}.".format(**scores)

    api.PostUpdate(message)

def notify(scores):
    # Only send notification if new score is greater than front page score
    if scores['front'] > scores['new']:
        return
    # Only send notification if we haven't done so in the last hour
    if (time.time() - db.fetch_notification_time()) < 60*60:
        return
    db.update_notification_time()
    tweet(scores)
