import requests
import json

from common.gloabals import Globals


def tweet_stream(observer, scheduler):
    uri = Globals.uri_tweet_stream
    headers = Globals.headers_tweet_stream
    req = requests.get(uri, stream=True, headers=headers)
    for tweet in req.iter_content(chunk_size=8192):
        try:
            tweet = tweet.decode("utf-8")
            data = json.loads(tweet)
            print(tweet)
            observer.on_next(data)
        except Exception as err:
            print('?', err)

    observer.on_completed()

