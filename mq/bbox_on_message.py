import json, logging, pika

from common.get_centroid_from_bbox import get_centroid_from_bbox
from common.get_temperature_from_lat_lon import get_temperature
from common.gloabals import Globals


def on_message(ch, method, properties, bbox):
    if Globals.sliding_ave_number < 2 or Globals.sliding_ave_number > 100:
        raise Exception("Globals.sliding_ave_number needs to be between 2 and 100")

    try:
        logging.info(f"geo listener on_message {bbox}")

        lat, lon = get_centroid_from_bbox(bbox)

        logging.info(f"geo centroid ({lat},{lon})")

        temp_data = get_temperature(lat, lon)

        if temp_data['success']:

            routing_key = temp_data['loc_key']
            logging.info(f"geo temp ({lat},{lon}) loc = {routing_key} temp_data = {temp_data}\n")

            # store temperature in list
            # { loc-key-a : [ temp, ...], loc-key-b : [ temp, ...] , ...
            temp = temp_data['temp']

            if not routing_key in Globals.mapGeoToTemp:
                logging.info(f"encountered new geo key {routing_key}")
                logging.info(f"connection on localhost {Globals.rabbit_host}")
                connection = pika.BlockingConnection(pika.ConnectionParameters(Globals.rabbit_host))
                channel = connection.channel()
                channel.queue_declare(queue=routing_key)
                logging.info(f"create list for key {routing_key}")
                Globals.mapGeoToTemp[routing_key] = []
            logging.info(f"Append temp temp{temp} to list {routing_key}")
            Globals.mapGeoToTemp[routing_key].append(temp)

            logging.info(f"queue-loc:{routing_key} last read:{temp} history: {Globals.mapGeoToTemp[routing_key]}")
            if Globals.is_console_printing:
                print('queue-loc', routing_key, 'last read', temp, 'history', Globals.mapGeoToTemp[routing_key])

            # append to Temperatures.csv file
            temp_file = open("../logs/Temperatures.txt", "a")
            temp_file.writelines(f"{routing_key},{temp}\n")
            temp_file.close()

            if len(Globals.mapGeoToTemp[routing_key]) >= Globals.sliding_ave_number:
                lst = Globals.mapGeoToTemp[routing_key]
                ave = sum(lst) / len(lst)

                if Globals.is_console_printing:
                    print(f"Computed average n:{Globals.sliding_ave_number} loc:{routing_key} ave:{ave}")

                logging.info(f" computed average over {Globals.sliding_ave_number},  publish on {routing_key} =  {ave}")

                # Write Average on location to File
                ave_file = open("../logs/Averages.txt", "a")
                ave_file.writelines(f"{routing_key},{ave}")
                ave_file.close()

                # Re-set Running Average List
                logging.info(f"reset running average list on location key {routing_key}")
                Globals.mapGeoToTemp[routing_key] = []

                # Publish Result to location queue for future usage
                logging.info(f"publish ave {ave}  to queue {routing_key}")
                Globals.basic_publish(exchange='',
                                      routing_key=routing_key,
                                      body=ave)
        else:
            logging.error(f"request on {lat} and {lon} did not return success {temp_data}")

    except Exception as e:
        print(f"geo listener on_message error {e}")
        logging.error(f"geo listener on_message error {e}")
