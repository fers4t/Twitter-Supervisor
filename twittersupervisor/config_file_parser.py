import json
import logging


class ConfigFileParser:

    # Default values
    default_db_file = "followers.db"

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config = json.load(open(config_file_name, 'r'))

    # TODO Check if the credentials work?
    def get_twitter_api_credentials(self):
        if "twitter_api" in self.config:
            if "username" not in self.config["twitter_api"]:
                raise KeyError("No \"twitter_api\" \"username\" found in {}".format(self.config_file_name))
            elif "consumer_key" not in self.config["twitter_api"]:
                raise KeyError("No \"twitter_api\" \"consumer_key\" key found in {}".format(self.config_file_name))
            elif "consumer_secret" not in self.config["twitter_api"]:
                raise KeyError("No \"twitter_api\" \"consumer_secret\" key found in {}".format(self.config_file_name))
            elif "access_token" not in self.config["twitter_api"]:
                raise KeyError("No \"twitter_api\" \"access_token\" key found in {}".format(self.config_file_name))
            elif "access_token_secret" not in self.config["twitter_api"]:
                raise KeyError("No \"twitter_api\" \"access_token_secret\" key found in {}".format(self.config_file_name))
            else:
                return self.config["twitter_api"]
        else:
            raise KeyError("No \"twitter_api\" key found in {}".format(self.config_file_name))

    def get_database_filename(self):
        try:
            return self.config["database_file"]
        except KeyError as e:
            logging.info("No database filename is specified in {}. Default value \"{}\" will be used."
                         .format(self.config_file_name, self.default_db_file))
            return self.default_db_file
