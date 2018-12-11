from unittest import TestCase, mock
from argparse import Namespace

from twittersupervisor import Messaging, TwitterApi, ConfigFileParser
from tests import test_data


class TestMessaging(TestCase):

    def setUp(self):
        self.twitter_api = TwitterApi(ConfigFileParser('config.json').get_twitter_api_credentials())

    def test_announce_follow_event(self):
        with mock.patch('twittersupervisor.TwitterApi.send_direct_message') as sdm:
            # Case quiet
            self.messaging = Messaging(self.twitter_api, Namespace(quiet=True))
            self.messaging.announce_follow_event(True, [test_data.twitter_user_id])
            sdm.assert_not_called()
            # Case "not quiet"
            self.messaging.args = Namespace(quiet=False)
            self.messaging.announce_follow_event(True, [test_data.twitter_user_id])
            sdm.assert_called_once()
