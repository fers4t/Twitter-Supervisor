import json
import logging


class ConfigFileParser:

    # Default values
    default_db_file = "followers.db"

    # TODO Put "existence check" of the config file here ?
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config = json.load(open(config_file_name, 'r'))

    # TODO Check if every required credential is here (and if they are Ok?)
    def get_twitter_api_credentials(self):
        try:
            return self.config["twitter_api"]
        except KeyError as e:
            logging.critical("No valid Twitter API credentials were found in \"{}\", please correct it and retry !"
                             .format(self.config_file_name))
            quit(1)

    def get_database_file(self):
        try:
            return self.config["database_file"]
        except KeyError as e:
            logging.info("No database filename is specified in {}. Default value \"{}\" will be used."
                         .format(self.config_file_name, self.default_db_file))
            return self.default_db_file
