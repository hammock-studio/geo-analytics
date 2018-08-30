import os
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret =os.environ['ACCESS_TOKEN_SECRET']

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(json.dumps(json.loads(data), indent=2, sort_keys=True))
        return True

    def on_error(self, status):
        print(status)

def tweets():
    tweets_listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, tweets_listener)
    stream.filter(locations=[-122.75,36.8,-121.75,37.8,-74,40,-73,41])
