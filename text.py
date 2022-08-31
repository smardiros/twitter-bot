import json
from pprint import pprint
from tokenize import String
from datetime import datetime
from pytz import timezone
import pickle

TWEETS_FILE = "tweet.json"

# 'Wed Aug 14 14:45:40 +0000 2019'
def twitter_date(date_string) -> datetime:
    """ Convert a twitter date string into a time struct
    date_string: string in twitter date format
    
    returns time.struct_time
    """

    format = "%a %b %d %X %z %Y"
    return datetime.strptime(date_string,format)


def is_rt(tweet_text) -> bool:
    """ Checks if the provided tweet text is a RT (starts with "RT")
    tweet_text: string
    
    returns: bool
    """

    return tweet_text[:3] == "RT "

def username_filter(tweet_text) -> str:
    """ Given the text of a tweet, return the text with usernames removed (usernames have the format @somestring)
    tweet_text: string  

    returns: string  
    """

    words = tweet_text.split()
    filtered_words = [word for word in words if word[0] != "@"]
    return " ".join(filtered_words)


def process_tweets(twitter_json, filter_usernames=True, filter_rts=False) -> list:
    """ Given a json object of the form provided by the twitter archive download, return a list of tweets and dates
    twitter_json: dict in twitter json format
    
    returns: list of (date, tweet) tuples
    """

    dated_tweets = []

    for tweet in twitter_json:
        date = tweet["tweet"]["created_at"]
        text = tweet["tweet"]["full_text"]

        if filter_rts and is_rt(text):
            continue

        if filter_usernames:
            text = username_filter(text)

        date = twitter_date(date)

        dated_tweets.append((date,text))

    return dated_tweets


def tweets_between(dated_tweets, start=None, end=None) -> list:
    """ Given a sorted list of dated tweets and a start and end dat
    return the tweets between those two dates. Default returns complete list
    
    dated_tweets: list of (time.time_struct, str) tuples
    start, end, time.time_struct
    
    returns: list of (time.time_struct, str) tuples
    """

    if start is None:
        start = dated_tweets[0][0]
    
    if end is None:
        end = dated_tweets[-1][0]

    filtered_tweets = []

    for date, tweet in dated_tweets:
        if date < start:
            continue
        if date > end:
            break

        filtered_tweets.append((date,tweet))

    return filtered_tweets

def save_tweets(dated_tweets, filename):
    """ Save a list of dated tweets to a file """
    with open(filename, 'wb') as file:
        pickle.dump(dated_tweets, file) 


if __name__ == "__main__":
    with open(TWEETS_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    tweets = process_tweets(data,filter_rts=True)
    tweets.sort()

    save_tweets(tweets, "dated_tweets.pickle")


        # date = datetime(2019, 8, 15)
        # est = timezone('US/Eastern')
        # start = est.localize(date)
        # tweets = tweets_between(tweets,start=start)




