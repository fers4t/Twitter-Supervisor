from twitter import Api, error
import logging


class TwitterApi:

    def __init__(self, twitter_credentials):
        try:
            self.username = twitter_credentials["username"]
            self.api = Api(consumer_key=twitter_credentials["consumer_key"],
                           consumer_secret=twitter_credentials["consumer_secret"],
                           access_token_key=twitter_credentials["access_token"],
                           access_token_secret=twitter_credentials["access_token_secret"])
        except KeyError as key_error:
            logging.critical("Invalid \"twitter_credentials\" argument: {}".format(key_error.args[0]))
            raise
        except TypeError as type_error:
            logging.critical("Incorrect \"twitter_credentials\" argument: {}".format(type_error.args[0]))
            raise

    def verify_credentials(self):
        try:
            return self.api.VerifyCredentials(None, True)
        except error.TwitterError as e:
            logging.error('An error happened while checking the Twitter API credentials validity: {}'.format(e.message))
            raise

    def get_followers_set(self):
        try:
            return set(self.api.GetFollowerIDs())
        except error.TwitterError as e:
            logging.critical('Twitter Supervisor is unable to get the user\'s followers IDs list: {}'.format(e.message))
            raise

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
