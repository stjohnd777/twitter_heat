import requests, json, abc, logging

from common.gloabals import Globals
from common.tweet_has_geo import tweet_has_geo


class Observer:
    """
    Interface for Observes
    """
    @abc.abstractmethod
    def notify(self, observable):
        pass


class PrintObserver(Observer):
    """
    Observer prints observable to stream
    """
    def notify(self, something):
        print(something)


class GeoObserver(Observer):
    def notify(self, tweet):
        try:
            if tweet_has_geo(tweet):
                bbox = tweet['includes']['places'][0]['geo']['bbox']
                print(bbox)
        except Exception as e:
            print(e)


def tweet_stream(receiver: Observer):
    """
    Forwards Tweet to the Observer 'receiver
    :param receiver:
    :return:
    """

    req = requests.get(Globals.uri_tweet_stream, stream=True, headers=Globals.headers_tweet_stream)

    for atweet in req.iter_content(chunk_size=8192):
        try:
            atweet = atweet.decode("utf-8")
            json_tweet = json.loads(atweet)
            logging.info(f"tweet received: {atweet}")
            if Globals.log_tweets :
                tweets_file = open(Globals.log_tweets, "a")
                tweets_file.writelines(atweet)
                tweets_file.close()

            if Globals.is_console_printing:
                print(atweet)
            receiver.notify(json_tweet)
        except :
            logging.error(f"error receiving tweet")

    logging.info(f"tweet stream ended {req}")


if __name__ == '__main__':
    geoHandler = GeoObserver()
    tweet_stream(geoHandler)
