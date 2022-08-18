import json
import tweepy

def get_keys(filename) -> dict:
    ''' Load json from file into dict '''
    try:
        with open(filename) as file:
            keys = json.load(file)
    except FileNotFoundError:
        print("File not found!")
    except json.decoder.JSONDecodeError:
        print("Invalid file!")
    
    return keys




if __name__ == "__main__":

    keys = get_keys("twitter_keys.json")
    consumer_key = keys["API key"]
    consumer_secret = keys["API key secret"]

    access_token = keys["Access token"]
    access_token_secret = keys["Access token secret"]

    bearer_token = keys["Bearer token"]

    client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

    client.create_tweet(text="Hello!")