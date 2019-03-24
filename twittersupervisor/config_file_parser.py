import json


class ConfigFileParser:

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config = json.load(open(config_file_name, 'r'))

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

    def get_database_credentials(self):
        if "postgresql" in self.config:
            if "host" not in self.config["postgresql"]:
                raise KeyError("No \"postgresql\" \"host\" found in {}".format(self.config_file_name))
            if "database" not in self.config["postgresql"]:
                raise KeyError("No \"postgresql\" \"database\" found in {}".format(self.config_file_name))
            if "user" not in self.config["postgresql"]:
                raise KeyError("No \"postgresql\" \"user\" found in {}".format(self.config_file_name))
            if "password" not in self.config["postgresql"]:
                raise KeyError("No \"postgresql\" \"password\" found in {}".format(self.config_file_name))
            else:
                return self.config["postgresql"]
        else:
            raise KeyError("No \"postgresql\" key found in {}".format(self.config_file_name))
