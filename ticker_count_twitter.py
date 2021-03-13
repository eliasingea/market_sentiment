import pymongo
import pandas as pd
from datetime import datetime

client = pymongo.MongoClient("localhost", 27017)
db = client.sentiment
twitter_collection = db.twitter

start = datetime.strptime("2021-03-13T00:00:00Z", '%Y-%m-%dT%H:%M:%SZ')
end = datetime.strptime("2021-03-13T21:00:00Z", '%Y-%m-%dT%H:%M:%SZ')

twitter_data = twitter_collection.find(
    { 
        "date_time": { 
            "$gte": start, 
            "$lt": end 
        } 
    }
)
df1 = pd.DataFrame(list(twitter_collection.find()), columns=['author', 'date_time', 'tweet', 'positive_sentiment', 'negative_sentiment', 'neutral_sentiment'])
df1.to_csv('export.csv')


df = pd.DataFrame(list(twitter_data), columns=['author', 'date_time', 'tweet', 'positive_sentiment', 'negative_sentiment', 'neutral_sentiment'])

df_tickers = pd.read_csv('ticker_list.csv') ## load list of tickers you want to analyze 
dollar_sign = "$"
output = pd.DataFrame({"ticker":['sample'], "count":[0],"dollar_count":[0],  "positive":[0], "negative": [0], "neutral": [0]})

### There is multiple reasons why analysis is done in the following way 
# You have check the number of times a ticker is present - a ticker can be present either by just ticker or after a dollar sign. 
# Especially in reddit, in comments you very rarely see a dollar sign 
# why we are calcualting the dollar sign is not to have false positives 
# if there are a lot of mentions for the ticker but not succeeding a $ sign it might be false positive 
# A lot of comments and tweets will only have zero sentiment which will pull down the average - so remove the zero sentiment data before calculating the sentiment 


for ticker in df_tickers['ticker']:
    a = df['tweet'].str.contains(" " + ticker + " ", case=False).sum()
    b = df['tweet'].str.contains(dollar_sign + ticker + " ", case=False, regex=False).sum()
    positive_sent = df[(df['tweet'].str.contains(dollar_sign + ticker + " ", case=False, regex=False))]['positive_sentiment'].mean()
    negative_sent = df[(df['tweet'].str.contains(dollar_sign + ticker + " ", case=False, regex=False))]['negative_sentiment'].mean()
    neutral_sent = df[(df['tweet'].str.contains(dollar_sign + ticker + " ", case=False, regex=False))]['neutral_sentiment'].mean()
    df_one_ticker = pd.DataFrame({"ticker":[ticker], "count":[a], "dollar_count":[b], "positive":[positive_sent], "negative": [negative_sent], "neutral": [neutral_sent]})
    output = output.append(df_one_ticker)


output.to_csv('march13_twitter_count.csv') ##location where you want the analysis output to be stored 

