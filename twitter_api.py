import twitter
import logging

import config

# API configuration
api = twitter.Api(consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token_key=config.access_token,
    access_token_secret=config.access_token_secret)

def get_followers_set():
	try:
		return set(api.GetFollowerIDs())
	except twitter.error.TwitterError as e:
		logging.critical('Unable to retrieve followers id list: {}'.format(e.message))
		return None;

def get_user(userId):
    try:
        return api.GetUser(userId)
    except twitter.error.TwitterError as e:
        logging.error('An error happened while searching for user n°{0}: {1}'.format(userId, e.message))
        return None;

def send_direct_message(text):
	try:
		return api.PostDirectMessage(text, screen_name = config.username)
	except twitter.error.TwitterError as e:
		logging.error('Unable to send direct message: {}'.format(e.message))
		return None;
