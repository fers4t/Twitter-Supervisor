# External dependencies
import argparse
import logging
# Custom dependencies
from twittersupervisor import ConfigFileParser, Database, Messaging, TwitterApi
import logging_config

# Command line parsing
parser = argparse.ArgumentParser()
parser.add_argument("--quiet", help="Disable the sending of direct messages", action="store_true")
args = parser.parse_args()

# Setup config
# TODO Retrieve config data from:
#  - command line arguments (config, and database files)
# Default values
config_file_name = "config.json"
log_file_name = "twitter_supervisor.log"

logging_config.set_logging_config(log_file_name)
config = ConfigFileParser(config_file_name)
twitter_api = TwitterApi(config.get_twitter_api_credentials())
database = Database(config.get_database_file())

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
    print("Thank you for using Twitter Supervisor, we are saving your followers"
          "for later use of the program...")
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
