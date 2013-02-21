#!/usr/bin/env python

import requests

HN_API_URL = "http://api.ihackernews.com/"
NUM_POINTS_TO_CONSIDER = 6

def fetch_scores(page_type):
    assert page_type in ['new', 'page']

    url = HN_API_URL + page_type
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception("Request for {} failed".format(url))
    score_data = request.json()
    scores = [item['points'] for item in score_data['items']]
    scores = scores[0:NUM_POINTS_TO_CONSIDER]

    return scores

if __name__ == '__main__':
    ss = fetch_scores('new')

    print(ss)




