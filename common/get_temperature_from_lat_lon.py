#!/usr/bin/env python
import logging, requests

from common.gloabals import Globals


def get_temperature(lat, lon):
    """
    Given lat and lon get the weather data from weather api
    :param lat:
    :param lon:
    :return:
    """

    logging.info(f"request weather data ( {lat} , {lon} )")
    uri = Globals.getWeatherUri(lat, lon)
    res = requests.get(uri)
    data = res.json()
    ret = {}

    if res.ok:
        if 'location' in data:
            location = data['location']
            if 'country' in location and 'region' in location and 'name' in location and 'current' in data:
                ret['country'] = data['location']['country']
                ret['region'] = data['location']['region']
                ret['name'] = data['location']['name']
                ret['loc_key'] = f"{ret['country']}-{ret['region']}-{ret['name']}"
            else:
                logging.info(f"no data ( {lat} , {lon} )")
                ret['success'] = False
        if 'current' in data:
            current = data['current']
            if 'temp_f' in current:
                ret['success'] = True
                ret['temp'] = current['temp_f']
            else:
                logging.info(f"no data ( {lat} , {lon} )")
                ret['success'] = False
        else:
            logging.info(f"no data ( {lat} , {lon} )")
            ret['success'] = False
    else:
        ret['success'] = False

    logging.info(f"request weather data ( {lat} , {lon} ) = {ret}")
    if Globals.is_console_printing:
        print(f"( {lat} , {lon} ) = {ret}")
    return ret
