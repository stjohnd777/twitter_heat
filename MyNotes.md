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

---
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

---

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

#### Weather
#### Base URL: http://api.weatherapi.com/v1
Castle Rock CO 39.3722° N, 104.8561° W
Latitude and Longitude (Decimal degree) e.g: q=39.3722,104.8561
API Key: 2d15b642528c4b7093412604221202
http://api.weatherapi.com/v1/forecast.json?key=2d15b642528c4b7093412604221202&q=39.3722,-104.8561&days=1&aqi=no&alerts=no


#### Solution Stack
- request
- pika
- RabbitMQ
- Docker

