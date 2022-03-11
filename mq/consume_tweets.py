#!/usr/bin/env python
import pika, sys, os, logging
from common.gloabals import Globals
from mq.bbox_on_message import on_message


class FetchTempMessageListener:

    def __init__(self, in_queue, callback):
        self.in_queue = in_queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(Globals.rabbit_host))
        logging.info(f"connection on localhost {Globals.rabbit_host}")
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=in_queue)
        logging.info(f"connection on localhost {in_queue}")
        self.channel.basic_consume(queue=in_queue, on_message_callback=callback, auto_ack=True)
        logging.info(f"ready to consuming on localhost on {in_queue}")

    def start(self):
        logging.info(f"consuming on localhost on {self.in_queue}")
        self.channel.start_consuming()


def start_msg_listener():
    logging.info("start_msg_listener")
    msg_driven_component = FetchTempMessageListener(Globals.tweets_with_geo_queue, on_message)
    msg_driven_component.start()


if __name__ == '__main__':
    try:
        logging.basicConfig(filename='../logs/twitter_consumer.log', level=logging.INFO)
        logging.info('start twitter_consumer')
        start_msg_listener()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        logging.info("KeyboardInterrupt")
        try:
            logging.info("Exiting")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
