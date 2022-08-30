import json
from pprint import pprint
from tokenize import String

TWEETS_FILE = "tweet_short.json"


def is_rt(tweet_text) -> bool:
    """ Checks if the provided tweet text is a RT (starts with "RT")
    tweet_text: string
    
    returns: bool
    """

    return tweet_text[:3] == "RT "

def filter_usernames(tweet_text) -> str:
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
        if filter_usernames:
            text = filter_usernames(tweet["tweet"]["full_text"])
        else:
            text = tweet["tweet"]["full_text"]
        dated_tweets.append((date,text))

    return dated_tweets





with open(TWEETS_FILE, 'r', encoding='utf-8') as file:
    data = json.load(file)
    tweets = process_tweets(data)
    pprint(tweets)



