import unittest
import config
from twittersupervisor.twitter_api import TwitterApi


class ApiTest (unittest.TestCase):

    def setUp(self):
        self.twitter_api = TwitterApi(config.USERNAME, config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN,
                                      config.ACCESS_TOKEN_SECRET)

    def test_get_followers(self):
        followers_set = self.twitter_api.get_followers_set()
        self.assertIsNotNone(followers_set)
        self.assertIsInstance(followers_set, set)

    def test_get_user(self):
        user = self.twitter_api.get_user(783214)  # @twitter user id
        self.assertIsNotNone(user)
