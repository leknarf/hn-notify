import time
import os
import json

import requests

FIREBASE_URL = os.environ['firebase_url']
FIREBASE_SECRET = os.environ['firebase_secret']

def __url(target):
    return FIREBASE_URL + target + '.json'

def _firebase_request(method, target, data=None):

    # Firebase requires data to be json encoded, not form encoded
    if data:
        data = json.dumps(data)
    try:
        req = requests.request(method, __url(target), data=data, params={'auth':FIREBASE_SECRET}, verify=False)
        req.raise_for_status()
        return req.json()
    except Exception as error:
        print("There was an exception connecting to Firebase."
                + "Method: '{}', URL: '{}', Data: '{}'.".format(method, __url(target), data))
        raise error

def write_scores(scores):
    scores['.priority'] = scores['time']
    _firebase_request('post', 'scores', data=scores)

def update_notification_time():
    data = {'last': int(time.time())}
    _firebase_request('put', 'notification_time', data=data)

def fetch_notification_time():
    try:
        result = _firebase_request('get', 'notification_time')
        return result['last']
    except:
        return 0
