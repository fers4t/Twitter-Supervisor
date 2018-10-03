import tweepy
import config

# API configuration
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

def getFollowersSet():
    return set(api.followers_ids(config.username));

def getUser(userId):
    try:
        return api.get_user(userId)
    except tweepy.TweepError as error :
        logging.error("An error happened when we tried to find user\
         %d: %s" % (user_id, error.reason));

def sendDirectMessage(text):
    api.send_direct_message(screen_name = config.username, text = text);
