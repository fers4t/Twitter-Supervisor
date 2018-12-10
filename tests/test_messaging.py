from unittest import TestCase, mock
from argparse import Namespace

import config
from twittersupervisor import Messaging, TwitterApi
from tests import test_data


class TestMessaging(TestCase):

    def setUp(self):
        self.twitter_api = TwitterApi(config.USERNAME, config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN,
                                      config.ACCESS_TOKEN_SECRET)

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
