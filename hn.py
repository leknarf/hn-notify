#!/usr/bin/env python

import time
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
                    time.sleep(5)
                    attempts += 1
        return wrapped_func
    return try_it

# The HN api frequently returns 500 errors, so we need to retry errors
@retry(10)
def fetch_scores(page_type):
    assert page_type in ['new', 'page']

    url = HN_API_URL + page_type
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception("Request for {} failed".format(url))
    score_data = request.json()
    scores = [item['points'] for item in score_data['items']]

    return scores

if __name__ == '__main__':
    highest_new_submissions = sorted(fetch_scores('new'))[0:NUM_POINTS_TO_CONSIDER]
    lowest_front_page_submissions = sorted(fetch_scores('page'))[-1 * NUM_POINTS_TO_CONSIDER:]

    print(highest_new_submissions)
    print(lowest_front_page_submissions)




