- ### Requirements
  - #### Continuously calculate the sliding avg of the temperatures 
    - High level correlate by location temperature averages ( by n ) across all locations.
  - ####  The number 'sliding average n' is configurable. 
    - The input value ‘n’ should be between 2 and 100
  - #### The output 2 files
    - file for the stream of temperatures in fahrenheit
    - file for the stream of the sliding averages.
  - ####  provide a high-level diagram of how you would deploy your solution


#### Tweets
- Twitter Streaming API Streams provides about 1% of all Tweets in real-time.
  - Needed Dev Account: Free
    - Get You Bearer Token: 
      - AAAAAAAAAAAAAAAAAAAAAAUuZQEAAAAAqaII840%2FTj93kIBq9aRxLZ%2FQc40%3DCU80Ke6nk8Phm8RdQJTmbfYpumNVTra7CFx0B8bQSNV8LL7ZVQ
    - Get Your API Key: 
      - B9ldwMgYsaPqk9g4pTkQl0gx9 
    - Get Your API Key Secret: 
      - P0Kzb0rnzyiRqlGsxCPsXVZa4ErsJrQgHDmJNX9c5TPoIuMYw7

### API
  - GET /2/tweets/sample/stream
    - https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream
    - https://api.twitter.com/2/tweets/sample/stream

### Curl
    - curl https://api.twitter.com/2/tweets/sample/stream -H "Authorization: Bearer $BEARER_TOKEN"

```python
    uri = 'https://api.twitter.com/2/tweets/sample/stream' \
          '?expansions=author_id,geo.place_id' \
          '&tweet.fields=geo' \
          '&user.fields=location' \
          '&place.fields=geo,country'
```
### Remark

Almost all the tweets do no contain geolocation. Maybe about 1%. This percentage will be calculated for my 
own sanity.

What I am getting back

```json
{
  'data': {
    'author_id': '4625949075', 
    geo': {'place_id': 'c0b8e8dc81930292'}, 
    'id': '1502328133806170115', 
    'text': 'aoty lolz https://t.co/6j06LMzRzM'
  }, 
  'includes': {
    'users': [{
          'id': '4625949075', 
          'location': 'Queens, NY', 
          'name': 'kas', 
          'username': 'niketotebag'}
    ], 
    'places': [{
      'country': 'United States', 
      'full_name': 'Baltimore, MD', 
      'geo': {'type': 'Feature', 'bbox': [-76.7115205, 39.197211, -76.529443, 39.372215], 'properties': {}}, 
      'id': 'c0b8e8dc81930292'}
    ]
  }
}

bbox = tweet['includes']['places'][0]['geo']['bbox']
[-76.7115205, 39.197211, -76.529443, 39.372215]

```
What I was expecting
```json
{
  "geo": {
    "type": "Point",
    "coordinates": [40.0160921, -105.2812196]
  },
  "coordinates": {
    "type": "Point",
    "coordinates": [-105.2812196, 40.0160921]
  }
}
```

     
     if 'geo' in tweet['data']:
         geo = tweet['data']['geo']
         if 'coordinates' in geo:
             lat = geo['coordinates'][0]
             lon = geo['coordinates'][1]
     elif 'coordinates' in tweet:
         coord = tweet['coordinates']
         if 'coordinates' in coord:
             lat = coord['coordinates'][1]
             lon = coord['coordinates'][0]
     else:
         pass

    print(data)
    ddata = data['data']
    print(ddata)
    geo = ddata['geo']
    print(geo)
    includes = data['includes']
    print(includes)
    users = includes['users']
    for u in users:
        location = u['location']
        print(location)


#### Since this is a streaming API one needs to iter on the content
```python
  req = requests.get(uri, stream=True, headers=headers)

  for tweet in req.iter_content(chunk_size=8192):
      try:
          tweet = tweet.decode("utf-8")
          # print(tweet)
          data = json.loads(tweet)
          print(data)
      except:
          pass

```

#### Tweet data, there are two classes of geographical metadata:
- Tweet location 
  - Available when user shares location at time of Tweet.
- Account Location 
  - Based on the ‘home’ location provided by user in their public profile. 
  - This is a free-form character field and may or may not contain metadata that can be geo-referenced.

#### Weather
Castle Rock CO 39.3722° N, 104.8561° W
Latitude and Longitude (Decimal degree) e.g: q=39.3722,104.8561
API Key: 2d15b642528c4b7093412604221202
http://api.weatherapi.com/v1/forecast.json?key=2d15b642528c4b7093412604221202&q=39.3722,-104.8561&days=1&aqi=no&alerts=no

#### Base URL: http://api.weatherapi.com/v1

#### The solution philosophy
- Tweets are asynchronous data streams thus Observables
- The Observer subscribe to the Tweet events
- The Observable notifies the subscribed Observers whenever an Tweet event occurs. 
- Because Observable sequences are streams we can filter, split, map, and compose 

#### Solution Stack
- request
- RxPy
- Docker

````json
ex = {
    "data": {
        "author_id": "568603156",
        "geo": {
            "coordinates": {
                "type": "Point",
                "coordinates": [
                    -53.45424491,
                    -33.69241331
                ]
            },
            "place_id": "f52168789ed14255"
        },
        "id": "1498469999064854529",
        "text": "No podía faltar el asadito de carnaval. en Barra del Chuy Uruguay https://t.co/Slxkfj9jZQ"
    },
    "includes": {
        "users": [
            {
                "id": "568603156",
                "location": "Montevideo uruguay ",
                "name": "diego langone",
                "username": "diegolangone72"
            }
        ],
        "places": [
            {
                "country": "Brazil",
                "full_name": "Chuí, Brasil",
                "geo": {
                    "type": "Feature",
                    "bbox": [
                        -53.522829,
                        -33.7429063,
                        -53.3015424,
                        -33.5561242
                    ],
                    "properties": {

                    }
                },
                "id": "f52168789ed14255"
            }
        ]
    }
}


````
curl --request GET 'https://api.twitter.com/2/tweets?ids=1136048014974423040&expansions=geo.place_id&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type' --header 'Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAAUuZQEAAAAAqaII840%2FTj93kIBq9aRxLZ%2FQc40%3DCU80Ke6nk8Phm8RdQJTmbfYpumNVTra7CFx0B8bQSNV8LL7ZVQ'

curl "https://api.twitter.com/2/tweets/sample/stream?expansions=geo.place_id&place.fields=name,country,country_code,place_type,contained_within,geo" -H "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAAUuZQEAAAAAqaII840%2FTj93kIBq9aRxLZ%2FQc40%3DCU80Ke6nk8Phm8RdQJTmbfYpumNVTra7CFx0B8bQSNV8LL7ZVQ"
````