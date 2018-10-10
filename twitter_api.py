import twitter
import logging

import config

# API configuration
api = twitter.Api(consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token_key=config.access_token,
    access_token_secret=config.access_token_secret)

def getFollowersSet():
    return set(api.GetFollowerIDs());

def getUser(userId):
    try:
        return api.GetUser(userId)
    except twitter.error.TwitterError as e:
        logging.error('An error happened while searching for user n°{0}: {1}'
        .format(userId, e.message))
        return None;

def sendDirectMessage(text):
    api.PostDirectMessage(text, screen_name = config.username);
