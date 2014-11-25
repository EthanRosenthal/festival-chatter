"""
Collect all tweets containg words in "filter" at bottom.
Store tweets in MongoDB

This code was basically totally stolen from
http://www.danielforsyth.me/analyzing-a-nhl-playoff-game-with-twitter/
"""

import tweepy
import sys
import pymongo

# The below authentication has been omitted for github
consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.tweetCount = 0

        self.db = pymongo.MongoClient().bonnaroo

    def on_status(self, status):
        status.text=str(unicode(status.text).encode("utf-8"))
        print status.text , "\n"

        data ={}
        data['text'] = status.text
        data['created_at'] = status.created_at
        data['geo'] = status.geo
        data['source'] = status.source

        self.db.Tweets.insert(data)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['bonnaroo','bonaroo','bonarroo','bonnarroo']) # Get all mispellings