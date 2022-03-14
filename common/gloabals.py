class Globals:

    # print to console
    is_console_printing = True

    log_tweets = True
    tweets_log = "../logs/tweets"

    # scaling on publishers
    number_tweet_publishers =1

    #scaling on consumers
    number_temp_listeners = 1

    # the twitter API returning geo loaction bbox
    uri_tweet_stream = 'https://api.twitter.com/2/tweets/sample/stream' \
          '?expansions=author_id,geo.place_id' \
          '&tweet.fields=geo' \
          '&user.fields=location' \
          '&place.fields=geo,country'

    # header for
    headers_tweet_stream = {
        "Content-Type": "application/json",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAAUuZQEAAAAAqaII840%2FTj93kIBq9aRxLZ%2FQc40%3DCU80Ke6nk8Phm8RdQJTmbfYpumNVTra7CFx0B8bQSNV8LL7ZVQ"
    }

    # siding average
    sliding_ave_number = 5

    # get the weather uri for location
    @staticmethod
    def getWeatherUri(lat,lon):
        uri_weather = f"http://api.weatherapi.com/v1/forecast.json?key=2d15b642528c4b7093412604221202&q={lat},{lon}&days=1&aqi=no&alerts=no"
        return uri_weather

    # rabbit host
    rabbit_host = "localhost"
    # queue for bounding box
    tweets_with_geo_queue = 'q-bbox'

    # application logs
    log_file_publisher = 'twitter_publisher.log'
    log_file_consumer = 'twitter_consumer.log'
    log_file_publisher_consumer = 'twitter_publisher_consumer.log'

    # functional file requirements
    file_temps = '../logs/Temperatures.csv'
    file_averages = '../logs/Averages.csv'

    # list for computing running averages
    mapGeoToTemp = {}