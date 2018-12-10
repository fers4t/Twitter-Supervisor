import unittest
import config
from twittersupervisor import TwitterApi
from tests import test_data


class ApiTest (unittest.TestCase):

    def setUp(self):
        self.twitter_api = TwitterApi(config.USERNAME, config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN,
                                      config.ACCESS_TOKEN_SECRET)

    def test_get_followers(self):
        followers_set = self.twitter_api.get_followers_set()
        self.assertIsNotNone(followers_set)
        self.assertIsInstance(followers_set, set)

    def test_get_user(self):
        user = self.twitter_api.get_user(test_data.twitter_user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Twitter')

    # TODO implement "def test_send_message(self, text)" when this test will be skipable
