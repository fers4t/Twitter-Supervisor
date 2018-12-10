from twitter import Api, error
import logging


class TwitterApi:
    def __init__(self, username, c_key, c_secret, access_token, access_token_secret):
        self.username = username
        self.api = Api(consumer_key=c_key,
                       consumer_secret=c_secret,
                       access_token_key=access_token,
                       access_token_secret=access_token_secret)

    def get_followers_set(self):
        try:
            return set(self.api.GetFollowerIDs())
        except error.TwitterError as e:
            logging.critical('Unable to retrieve followers id list: {}'.format(e.message))
            return None

    def get_user(self, user_id):
        try:
            return self.api.GetUser(user_id)
        except error.TwitterError as e:
            logging.error('An error happened while searching for user n°{0}: {1}'.format(user_id, e.message))
            return None

    def send_direct_message(self, text):
        logging.info('Sending direct message: \"{}\"'.format(text))
        try:
            return self.api.PostDirectMessage(text, screen_name=self.username)
        except error.TwitterError as e:
            logging.error('Unable to send direct message: {}'.format(e.message))
            return None
