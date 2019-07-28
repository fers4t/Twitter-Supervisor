from twitter import Api, error
import logging


class TwitterApi:

    DESTROY_STATUS_ENDPOINT = "https://api.twitter.com/1.1/statuses/destroy/:id.json"
    DESTROY_FAVORITE_ENDPOINT = "https://api.twitter.com/1.1/favorites/destroy.json"

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

    def check_rate_limit(self, endpoint_url):
        try:
            return self.api.CheckRateLimit(endpoint_url)
        except error.TwitterError as e:
            logging.critical('An error happened when rate limit of endpoint {} was checked: {}'.format(endpoint_url, e.message))
            return None

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

    def get_user_timeline(self):
        try:
            return self.api.GetUserTimeline(screen_name=self.username, count=200, since_id=20)
        except error.TwitterError as e:
            logging.error('Unable to get user @{0} timeline: {1}'.format(self.username, e.message))
            return None

    def get_favorites(self):
        try:
            return self.api.GetFavorites(screen_name=self.username, count=200, since_id=20)
        except error.TwitterError as e:
            logging.error('Unable to get user @{0} favorites: {1}'.format(self.username, e.message))
            return None

    def delete_status(self, status_id):
        try:
            return self.api.DestroyStatus(status_id)
        except error.TwitterError as e:
            logging.error('Unable to delete status n°{0} because of error: {1}'.format(status_id, e.message))
            return None

    def delete_favorite(self, status_id):
        try:
            return self.api.DestroyFavorite(status_id=status_id)
        except error.TwitterError as e:
            logging.error('Unable to delete status n°{0} because of error: {1}'.format(status_id, e.message))
            return None

    def delete_old_stuff(self, items_type, items, start, end):
        deleted_items = []
        for i in range(start, end):
            if items_type == 'statuses':
                deleted_status = self.delete_status(items[i].id)
                if deleted_status is not None:
                    deleted_items.append(deleted_status)
                logging.debug('Delete tweet n°{0} from {1}'.format(items[i].id, items[i].user.screen_name))
            elif items_type == 'favorites':
                deleted_status = self.delete_favorite(items[i].id)
                if deleted_status is not None:
                    deleted_items.append(deleted_status)
                logging.debug('Delete favorite n°{0} from {1}'.format(items[i].id, items[i].user.screen_name))
        return deleted_items
