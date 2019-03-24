from unittest import TestCase

from tests import shared_test_data
from twittersupervisor import ConfigFileParser


class TestConfigFileParser(TestCase):
    CORRECT_TWITTER_API_CONFIG = {'username': 'ausername', 'consumer_key': 'aconsumerkey',
                                  'consumer_secret': 'aconsumersecret',
                                  'access_token': 'anaccesstoken',
                                  'access_token_secret': 'anaccesstokensecret'}
    CORRECT_DB_CONFIG = {
        "user": "auser",
        "password": "apassword",
        "host": "ahost",
        "database": "adatabase"
    }

    def setUp(self):
        # Complete config file case
        self.complete_config = ConfigFileParser(shared_test_data.COMPLETE_CONFIG_FILE)
        # Missing "database_name" entry case
        self.incomplete_database_config = ConfigFileParser("test_data/incomplete_database_config.json")
        # Missing "twitter_api" sub-key case
        self.missing_twitter_api_sub_key = ConfigFileParser("test_data/missing_consumer_key_config.json")

    def test_get_twitter_api_credentials(self):
        self.assertEqual(self.complete_config.get_twitter_api_credentials(),
                         TestConfigFileParser.CORRECT_TWITTER_API_CONFIG)
        self.assertRaises(KeyError, self.missing_twitter_api_sub_key.get_twitter_api_credentials)
        self.assertEqual(self.incomplete_database_config.get_twitter_api_credentials(),
                         TestConfigFileParser.CORRECT_TWITTER_API_CONFIG)

    def test_get_database_file(self):
        self.assertEqual(self.complete_config.get_database_credentials(), TestConfigFileParser.CORRECT_DB_CONFIG)
        self.assertRaises(KeyError, self.incomplete_database_config.get_database_credentials)
        self.assertEqual(self.missing_twitter_api_sub_key.get_database_credentials(), TestConfigFileParser.CORRECT_DB_CONFIG)
