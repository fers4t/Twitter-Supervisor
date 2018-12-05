import unittest

from twittersupervisor import twitter_api


class ApiTest (unittest.TestCase):

    def test_get_followers(self):
        followers_set = twitter_api.get_followers_set()
        self.assertIsNotNone(followers_set)
        self.assertIsInstance(followers_set, set)

    def test_get_user(self):
        user = twitter_api.get_user(783214)  # @twitter user id
        self.assertIsNotNone(user)
