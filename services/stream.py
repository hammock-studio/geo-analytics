import os
import json
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(os.environ['ES_URL'])

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

def cast_time_format(time_str):
    in_format = '%a %b %d %H:%M:%S +0000 %Y'
    out_format = '%Y-%m-%dT%H:%M:%S'
    return time.strftime(out_format, time.strptime(time_str, in_format))

def source_record_to_mapping(tweet):
    sourced_record = {}
    sourced_record['user'] = {}
    sourced_record['place'] = {}
    sourced_record['place']['location'] = {}

    sourced_record['created_at'] = cast_time_format(tweet['created_at'])
    sourced_record['timestamp_ms'] = tweet['timestamp_ms']
    sourced_record['lang'] = tweet['lang']
    sourced_record['source'] = tweet['source']
    sourced_record['text'] = tweet['text']
    sourced_record['hashtags'] = tweet['entities']['hashtags']

    sourced_record['place']['location']['coordinates'] = tweet['place']['bounding_box']['coordinates']
    sourced_record['place']['location_point'] = tweet['place']['bounding_box']['coordinates'][0][0]
    sourced_record['place']['location']['type'] = 'polygon'
    sourced_record['place']['country'] = tweet['place']['country']
    sourced_record['place']['country_code'] = tweet['place']['country_code']
    sourced_record['place']['id'] = tweet['place']['id']
    sourced_record['place']['name'] = tweet['place']['name']
    sourced_record['place']['full_name'] = tweet['place']['full_name']
    sourced_record['place']['place_type'] = tweet['place']['place_type']

    sourced_record['user']['id'] = tweet['user']['id']
    sourced_record['user']['created_at'] = cast_time_format(tweet['user']['created_at'])
    sourced_record['user']['name'] = tweet['user']['name']
    sourced_record['user']['description'] = tweet['user']['description']
    sourced_record['user']['location'] = tweet['user']['location']
    sourced_record['user']['profile_image_url_https'] = tweet['user']['profile_image_url_https']
    sourced_record['user']['lang'] = tweet['user']['lang']
    sourced_record['user']['followers_count'] = tweet['user']['followers_count']

    return sourced_record


def format_tweets_to_actions(index, doc, tweets):
    actions = []

    for tweet in tweets:
        try:
            action = {
                "_op_type": "index",
                "_index": index,
                "_type": doc,
                "_source": source_record_to_mapping(tweet)
            }

            actions.append(action)
        except:
            print("failed")


    return actions

def index_data(es, index, doc, tweets):
    actions = format_tweets_to_actions(index, doc, tweets)
    helpers.bulk(es, actions)


class StdOutListener(StreamListener):
    def __init__(self, es, index, doc):
        self.es = es
        self.doc = doc
        self.index = index
        self.tweets = []

    def on_data(self, data):
        if len(self.tweets) > 10:
            index_data(self.es, self.index, self.doc, self.tweets)
            self.tweets = []
        else:
            self.tweets.append(json.loads(data))

        return True

    def on_error(self, status):
        print(status)

def tweets(es, inedx, doc):
    tweets_listener = StdOutListener(es, inedx, doc)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, tweets_listener)
    stream.filter(locations=[-122.75,36.8,-121.75,37.8,-74,40,-73,41])

tweets(es, 'geo-analytics', 'tweets') # access from webpage to switch on/off
