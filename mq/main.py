import os, sys, logging, time
from threading import Thread
from mq.consume_tweets import start_msg_listener
from common.gloabals import Globals
from mq.publish_tweet import start_tweet_publisher

if __name__ == '__main__':

    logging.basicConfig(filename='../logs/both_publisher_consumer.log', level=logging.INFO)
    logging.info('String Main')

    try:

        for instance in range(0, Globals.number_tweet_publishers):
            t = Thread(target=start_tweet_publisher, daemon=True)
            t.start()
            logging.info(f"started start_tweet_publisher thread")

        for instance in range(0, Globals.number_temp_listeners):
            t = Thread(target=start_msg_listener, daemon=True)
            t.start()
            logging.info(f"started start_tweet_consumer thread")

        # run for an hr
        time.sleep( 60* 60)

        logging.info("Exiting")

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
