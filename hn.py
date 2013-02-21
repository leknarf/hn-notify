#!/usr/bin/env python

from __future__ import division
import time

import numpy
import requests

HN_API_URL = "http://api.ihackernews.com/"
NUM_POINTS_TO_CONSIDER = 6

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
@retry(15)
def fetch_scores(page_type):
    assert page_type in ['new', 'page']

    url = HN_API_URL + page_type
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception("Request for {} failed".format(url))
    score_data = request.json()
    scores = [item['points'] for item in score_data['items']]

    return scores

def pickup_ratio():
    highest_new_submissions = sorted(fetch_scores('new'), reverse=True)[:NUM_POINTS_TO_CONSIDER]
    lowest_front_page_submissions = sorted(fetch_scores('page'))[:NUM_POINTS_TO_CONSIDER]

    avg_new = numpy.median(highest_new_submissions)
    avg_front = numpy.median(lowest_front_page_submissions)

    return avg_new / avg_front


if __name__ == '__main__':
    print("Current pickup ratio is: {}".format(pickup_ratio()))
