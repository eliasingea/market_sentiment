from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
import datetime
from unidecode import unidecode
import time
import pandas as pd
import json
import pymongo
from dotenv import load_dotenv
import os
from analyzeSentiment import returnSentiment

load_dotenv("env/keys.env")

client = pymongo.MongoClient("localhost", 27017)
db = client.sentiment
twitter_collection = db.twitter


# Insert your twitter API key here 
ckey=os.getenv('TWITTER_KEY')
csecret=os.getenv('TWITTER_SECRET')
atoken=os.getenv('TWITTER_ACCESS_TOKEN')
asecret=os.getenv('TWITTER_TOKEN_SECRET')


class listener(StreamListener):
    def on_status(self,data):
        try: 
            text = data.extended_tweet["full_text"] 
        except AttributeError:
            text = data.text
        created_at = data.created_at
        author = str(data.author.screen_name)
        vs = returnSentiment(unidecode(text))
        sentiment = vs
        twitter_collection.insert({
            "date_time": created_at, 
            "author": author, 
            "tweet": text, 
            "positive_sentiment": sentiment["positive"],
            "neutral_sentiment": sentiment["neutral"],
            "negative_sentiment": sentiment["negative"]
        })       
    def on_error(self,status):
        print(status)

## Connecting to twitter and establishing a live stream 
while True:
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener(), tweet_mode='extended')
        twitterStream.filter(track=["$AAPL", "$TSLA", "$GME"]) #this tracks any tweet with a $ symbol. Unlike Reddit, a large proportion of twitter users use $ before the stock tickers
    except Exception as e:
        print(str(e))
        time.sleep(10)
