import json, sys, os, pika, logging

from common.gloabals import Globals
from common.tweet_has_geo import tweet_has_geo
from common.tweet_stream import Observer, tweet_stream


class GeoTweetObserver(Observer):
    """
    Publish Tweets with Geo location bbox information to Rabbit Queue
    """

    def __init__(self, queue_name):
        try:
            self.queue_name = queue_name
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue_name)
        except Exception as e:
            logging.error(e)
            sys.exit(0)

    def notify(self, tweet):
        try:
            if tweet_has_geo(tweet):
                bbox = tweet['includes']['places'][0]['geo']['bbox']
                if Globals.is_console_printing:
                    print(bbox)
                _bbox = json.dumps(bbox)
                self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=_bbox)
        except Exception as e:
            logging.error(e)

    def close(self):
        self.connection.close()


def start_tweet_publisher():
    geo_observer = GeoTweetObserver(Globals.tweets_with_geo_queue)
    tweet_stream(geo_observer)


if __name__ == '__main__':
    try:
        logging.basicConfig(filename='../logs/twitter_publisher.log', level=logging.INFO)
        logging.info('starting  twitter_publisher')
        start_tweet_publisher()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        logging.info("KeyboardInterrupt")
        try:
            logging.info("Exiting")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
