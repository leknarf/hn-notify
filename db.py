import time
import os

import firebase

FIREBASE_URL = os.environ['firebase_url']

def write_scores(scores):
    db = firebase.Firebase(FIREBASE_URL + 'scores')
    db.push(scores)

def update_notification_time():
    db = firebase.Firebase(FIREBASE_URL + 'notification_time')
    db.put({'last': int(time.time())})

def fetch_notification_time():
    db = firebase.Firebase(FIREBASE_URL + 'notification_time')
    result = db.get()()

    return result['last'] if result else 0
