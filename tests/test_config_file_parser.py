from unittest import TestCase

from twittersupervisor import ConfigFileParser


class TestConfigFileParser(TestCase):

    CORRECT_TWITTER_API_CONFIG = {'username': 'ausername', 'consumer_key': 'aconsumerkey',
                                  'consumer_secret': 'aconsumersecret',
                                  'access_token': 'anaccesstoken',
                                  'access_token_secret': 'anaccesstokensecret'}
    CORRECT_DB_NAME = 'a_database_file.db'

    def setUp(self):
        # Complete config file case
        self.complete_config = ConfigFileParser("test_data/complete_config.json")
        # Missing "database_name" entry case
        self.missing_database = ConfigFileParser("test_data/missing_database_config.json")
        # Missing "twitter_api" sub-key case
        self.missing_twitter_api_sub_key = ConfigFileParser("test_data/missing_consumer_key_config.json")

    def test_get_twitter_api_credentials(self):
        self.assertEqual(self.complete_config.get_twitter_api_credentials(),
                         TestConfigFileParser.CORRECT_TWITTER_API_CONFIG)
        self.assertRaises(KeyError, self.missing_twitter_api_sub_key.get_twitter_api_credentials)
        self.assertEqual(self.missing_database.get_twitter_api_credentials(),
                         TestConfigFileParser.CORRECT_TWITTER_API_CONFIG)

    def test_get_database_file(self):
        self.assertEqual(self.complete_config.get_database_filename(), TestConfigFileParser.CORRECT_DB_NAME)
        self.assertEqual(self.missing_twitter_api_sub_key.get_database_filename(), ConfigFileParser.DEFAULT_DB_FILE)
        self.assertEqual(self.missing_database.get_database_filename(), ConfigFileParser.DEFAULT_DB_FILE)
