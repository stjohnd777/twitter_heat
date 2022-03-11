class Globals:

    is_console_printing = True

    number_tweet_publishers =1

    number_temp_listeners = 1

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

    rabbit_host = "localhost"

    tweets_with_geo_queue = 'Q2'

    log_file_publisher = 'twitter_publisher.log'

    log_file_consumer = 'twitter_consumer.log'


    mapGeoToTemp = {}