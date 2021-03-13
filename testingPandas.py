#%%
import pandas as pd
import pymongo
#%%
client = pymongo.MongoClient("localhost", 27017)
db = client.sentiment
twitter_collection = db.twitter

#%%
col_df = pd.DataFrame(list(twitter_collection.find()), columns=['author', 'date_time', 'tweet', 'sentiment'])
col_df.drop(0)
#%%
def return_sent(sentiment):
    if('positive' not in sentiment):
        return 0
    print(sentiment)
    if(sentiment['positive'] > sentiment['negative']):
        return sentiment['positive'] + 1
    elif (sentiment['negative'] > sentiment['positive']):
        return sentiment['negative']

def averagePositive(sentiment):
    count = 0
    sum = 0
    for sent in sentiment:
        if sent > 1:
            sum += sent
            count += 1
    return sum / count

def averageNegative(sentiment): 
    count = 0
    sum = 0
    for sent in sentiment:
        if sent < 1:
            sum += sent
            count += 1
    return sum / count

# %%
col_df = col_df.dropna()
#col_df['sentiment_percentage'] = col_df.apply(lambda x: return_sent(x.sentiment), axis=1); 
# %%
positive_percent = abs(1 - averagePositive(col_df['sentiment_percentage']))
negative_percent = averageNegative(col_df['sentiment_percentage'])
col_df.plot(x='date_time', y='sentiment_percentage', kind='bar')
#col_df = col_df.drop(0)
# col_df = col_df.drop(19)
# col_df["date_time"] = pd.to_datetime(col_df["date_time"])

# %%
MAX_DF_LENGTH = 100
def df_resample_sizes(df, maxlen=MAX_DF_LENGTH):
    ind1 = df['date_time'].iat[-1]
    ind0 = df['date_time'].iat[0]
    df = df.set_index(['date_time'])
    vol_df = df.copy()
    vol_df['volume'] = 1
    print(type(ind1))
    print(ind0)
    ms_span = (ind1 - ind0).seconds * 1000
    rs = int(ms_span / maxlen)
    print(type(df.index))
    df1 = df.resample('{}ms'.format(int(rs))).sum()
    df1.dropna(inplace=True)
    vol_df = vol_df.resample('{}ms'.format(int(rs))).sum()
    vol_df.dropna(inplace=True)
    df1 = df1.join(vol_df['volume'])
    return df1

# %%
type(col_df.index[0])
new_df = df_resample_sizes(col_df)
# %%
print(new_df)
# %%
