# External dependencies
import argparse
import logging
import os.path
# Custom dependencies
from twittersupervisor import ConfigFileParser, Database, Messaging, TwitterApi
import logging_config

# Default values
config_file_name = "config.json"
log_file_name = "twitter_supervisor.log"

# Command line parsing
parser = argparse.ArgumentParser()
parser.add_argument("--quiet", help="Disable the sending of direct messages", action="store_true")
parser.add_argument("--config", help="Specify which configuration file to use. It must be a JSON file.",
                    nargs=1, metavar="config_file")
parser.add_argument("--database", help="Specify which SQLite .db file to use", nargs=1, metavar="database_file")
args = parser.parse_args()

# Setup config
if args.config:
    if os.path.isfile(args.config[0]):
        config_file_name = args.config[0]
    else:
        logging.critical("Incorrect argument: %s is not file or does not exist.", args.config[0])
        quit(1)
logging_config.set_logging_config(log_file_name)
config = ConfigFileParser(config_file_name)
twitter_api = TwitterApi(config.get_twitter_api_credentials())
database = None
if args.database:
    database = Database(args.database[0])
else:
    database = Database(config.get_database_file())

logging.info("Configuration loaded from: {}".format(config.config_file_name))
logging.info("Data saved in: {}".format(database.database_name))
logging.debug("Username: {}".format(twitter_api.username))

# Main function---------------------------------------------------------------------------------------------------------
logging.info('Twitter Supervisor launched!')

# Retrieve the previous followers set
previous_followers = database.get_previous_followers_set()
previous_followers_number = len(previous_followers)

# Get the current followers set
current_followers = twitter_api.get_followers_set()
followers_number = len(current_followers)
logging.info("Current number of followers: {}".format(followers_number))

# Comparison of the two sets of followers
new_followers = current_followers - previous_followers
traitors = previous_followers - current_followers

# If there are no followers saved in DB, we consider it is the first use
if previous_followers_number == 0:
    print("Thank you for using Twitter Supervisor, we are saving your followers for later use of the program...")
else:
    logging.info("Previous number of followers: {}".format(previous_followers_number))
    messaging = Messaging(twitter_api, args)
    messaging.announce_follow_event(True, new_followers)
    messaging.announce_follow_event(False, traitors)

# Save the followers set in DB if there is change
if len(new_followers) == 0 and len(traitors) == 0:
    logging.info("\"[...] nihil novi sub sole.\" - Ecclesiastes 1:9")
else:
    database.update_followers_table(new_followers, traitors)

logging.info("Twitter Supervisor ran successfully!")
