import json, logging, pika
from common.get_temperature_from_lat_lon import get_temperature
from common.gloabals import Globals


def on_message(ch, method, properties, bbox):

    try:
        logging.info( f"geo listener on_message {bbox}")

        bbox = bbox.decode("utf-8")
        bbox = json.loads(bbox)
        lat = (bbox[0] + bbox[2]) / 2
        lon = (bbox[1] + bbox[3]) / 2
        logging.info(f"geo centroid ({lat},{lon})")

        temp_data = get_temperature(lat, lon)
        logging.info(f"geo listener centroid ({lat},{lon}) temp = {temp_data}")

        if temp_data['success']:

            temp = temp_data['temp']
            routing_key = temp_data['loc_key']

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


            # Write Temperatures filet
            temp_file = open("../logs/Temperatures.txt", "a")
            temp_file.writelines(f"{routing_key},{temp}")
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

                # Rested Running Average List
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
