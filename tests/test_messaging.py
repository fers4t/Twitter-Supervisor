from unittest import TestCase, mock
from argparse import Namespace
from twitter import User
from twittersupervisor import Messaging, TwitterApi, ConfigFileParser
from tests import shared_test_data


class TestMessaging(TestCase):

    def setUp(self):
        self.twitter_api = TwitterApi(ConfigFileParser(shared_test_data.COMPLETE_CONFIG_FILE)
                                      .get_twitter_api_credentials())

    # TODO Improve this test case (correct message, special characters case...)
    def test_announce_follow_event(self):
        with mock.patch('twittersupervisor.TwitterApi.get_user') as get_user:
            get_user.return_value = User(id=783214, name="Twitter")
            with mock.patch('twittersupervisor.TwitterApi.send_direct_message', unsafe=True) as sdm:
                # Case quiet
                self.messaging = Messaging(self.twitter_api, Namespace(quiet=True))
                self.messaging.announce_follow_event(True, [shared_test_data.TWITTER_USER_ID])
                sdm.assert_not_called()
                # Case "not quiet"
                self.messaging.args = Namespace(quiet=False)
                self.messaging.announce_follow_event(True, [shared_test_data.TWITTER_USER_ID])
                sdm.assert_called_once()
