import logging


def tweet_has_geo(tweet):
    """
    return True is geo data present otherwise False
    :param tweet:
    :return:
    """
    # return tweet['includes']['places'][0]['geo']['bbox']

    if 'includes' in tweet:
        includes = tweet['includes']
        if 'places' in includes:
            places = includes['places']
            for place in places:
                if 'geo' in place:
                    geo = place['geo']
                    if 'bbox' in geo:
                        logging.info(f"True tweet has goe data {geo['bbox']}")
                        return True
    logging.info("False: tweet has no geo data")
    return False
