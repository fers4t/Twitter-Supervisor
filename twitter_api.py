from twitter import Api, error
import logging

import config

# API configuration
api = Api(consumer_key=config.CONSUMER_KEY,
          consumer_secret=config.CONSUMER_SECRET,
          access_token_key=config.ACCESS_TOKEN,
          access_token_secret=config.ACCESS_TOKEN_SECRET)


def get_followers_set():
    try:
        return set(api.GetFollowerIDs())
    except error.TwitterError as e:
        logging.critical('Unable to retrieve followers id list: {}'.format(e.message))
        return None


def get_user(user_id):
    try:
        return api.GetUser(user_id)
    except error.TwitterError as e:
        logging.error('An error happened while searching for user n°{0}: {1}'.format(user_id, e.message))
        return None


def send_direct_message(text):
    logging.info('Sending direct message: \"{}\"'.format(text))
    try:
        return api.PostDirectMessage(text, screen_name=config.USERNAME)
    except error.TwitterError as e:
        logging.error('Unable to send direct message: {}'.format(e.message))
        return None
