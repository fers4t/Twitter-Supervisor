from unittest import TestCase
from twittersupervisor import ConfigFileParser, TwitterApi
from tests import test_data


class ApiTest (TestCase):

    def setUp(self):
        self.twitter_api = TwitterApi(ConfigFileParser('config.json').get_twitter_api_credentials())

    def test_get_followers(self):
        followers_set = self.twitter_api.get_followers_set()
        self.assertIsNotNone(followers_set)
        self.assertIsInstance(followers_set, set)

    def test_get_user(self):
        user = self.twitter_api.get_user(test_data.twitter_user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Twitter')

    # TODO implement "def test_send_message(self, text)" when this test will be skipable
