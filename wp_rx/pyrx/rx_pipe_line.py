from rx import create
from rx import operators as op

from common.tweet_has_geo import tweet_has_geo
from tweet_source import tweet_stream
from common.get_temperature_from_lat_lon import get_temperature


def start_pipe_line(handler):
    source = create(tweet_stream)

    def map_temp(tweet):
        print(tweet)
        bbox = tweet['includes']['places'][0]['geo']['bbox']
        lat = (bbox[0] + bbox[2]) / 2
        lon = (bbox[1] + bbox[3]) / 2
        temp_data = get_temperature(lat, lon)
        return temp_data

    source.pipe(
        op.filter(tweet_has_geo)
        , op.map(map_temp)
        # , op.group_by(lambda i: i['loc_key'])
        # , op.flat_map(lambda grp: grp.pipe(op.to_list())),
    ).subscribe(
        on_next=handler,
        on_completed=completion_handler
    )


def completion_handler(extended_tweet):
    print(extended_tweet)

# start_pipe_line(complete_handler)
