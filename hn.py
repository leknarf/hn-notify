#!/usr/bin/env python

from __future__ import division
import time

import requests

import db
import notify

HN_API_URL = "http://api.ihackernews.com/"

# Based on http://stackoverflow.com/questions/567622/is-there-a-pythonic-way-to-try-something-up-to-a-maximum-number-of-times
def retry(max_attempts):
    def try_it(func):
        def wrapped_func(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if attempts >= max_attempts:
                        raise error
                    print("{}. Retrying... attempt {}".format(error, attempts))
                    time.sleep(10)
                    attempts += 1
        return wrapped_func
    return try_it

# The HN api frequently returns 500 errors, so we need to retry errors
@retry(20)
def fetch(page_type):
    assert page_type in ['new', 'page']

    url = HN_API_URL + page_type
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception("Request for {} failed".format(url))
    score_data = request.json()
    scores = [item['points'] for item in score_data['items']]

    return scores

def calculate():
    highest_new_submissions = sorted(fetch('new'), reverse=True)
    lowest_front_page_submissions = sorted(fetch('page'))

    # Report the second-highest and second-lowest score
    new_score = highest_new_submissions[1]
    front_score = lowest_front_page_submissions[1]

    return {'new': new_score, 'front': front_score, 'time': int(time.time())}

if __name__ == '__main__':
    while True:
        #try:
        scores = calculate()
        db.write_scores(scores)
        notify.notify(scores)
        print("Current median scores are: {}".format(scores))
        #except Exception as error:
            #print("ERROR: {}".format(error))
        time.sleep(60*5)