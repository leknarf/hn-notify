#!/usr/bin/env python

from __future__ import division
import time

import requests
import grequests

import db
import notify

HN_API_URL = "https://hacker-news.firebaseio.com/v0"

STORIES_ON_PAGE = 30
FETCH_WINDOW = 200

def item_url(item_id):
    url = "{HN_API_URL}/item/{item_id}.json".format(HN_API_URL=HN_API_URL, item_id=item_id)
    return url

def fetch_scores_for_ids(item_ids):
    urls = [item_url(item_id) for item_id in item_ids]
    requests = grequests.map(grequests.get(url) for url in urls)
    successful_requests = [request for request in requests if request.status_code == 200]
    jsons = [request.json() for request in successful_requests]
    for json in jsons:
        if 'type' not in json.keys():
            print(json)
    stories = [json for json in jsons if json['type'] == 'story']
    active_stories = [story for story in stories if 'score' in story.keys()]
    scores = [story['score'] for story in active_stories]
    return scores

def fetch_front_page_ids():
    url = HN_API_URL + '/topstories.json'
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception("Request for {} failed".format(url))
    front_page_item_ids = request.json()
    return front_page_item_ids

def fetch_newest_id():
    url = HN_API_URL + '/maxitem.json'
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception("Request for {} failed".format(url))
    return request.json()

def fetch_newest_stories():
    max_id = fetch_newest_id()
    scores = []
    while len(scores) < STORIES_ON_PAGE:
        target_ids = range(max_id, max_id - FETCH_WINDOW, -1)
        target_urls = [item_url(target_id) for target_id in target_ids]
        scores += fetch_scores_for_ids(target_ids)
        max_id -= FETCH_WINDOW
    return scores

def calculate():
    front_page_scores = fetch_scores_for_ids(fetch_front_page_ids())[:STORIES_ON_PAGE]
    print("Front page scores: {}".format(front_page_scores))
    new_page_scores = fetch_newest_stories()[:STORIES_ON_PAGE]
    print("New page scores: {}".format(new_page_scores))

    highest_new_submissions = sorted(new_page_scores, reverse=True)
    lowest_front_page_submissions = sorted(front_page_scores)

    # Report the second-highest and second-lowest score
    new_score = highest_new_submissions[1]
    front_score = lowest_front_page_submissions[1]

    return {'new': new_score, 'front': front_score, 'time': int(time.time())}

if __name__ == '__main__':
    while True:
        try:
            scores = calculate()
            db.write_scores(scores)
            notify.notify(scores)
            print("Current 2nd highest/lowest scores are: {}".format(scores))
        except Exception as error:
            print("ERROR: {}".format(error))
        time.sleep(60*5)
