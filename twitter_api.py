import twitter
import config

# API configuration
api = twitter.Api(consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token_key=config.access_token,
    access_token_secret=config.access_token_secret)

def getFollowersSet():
    return set(api.GetFollowerIDs());

def getUser(userId):
    return api.GetUser(userId);

def sendDirectMessage(text):
    api.PostDirectMessage(text, screen_name = config.username);
