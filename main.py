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

# Command line parsing--------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--quiet", help="Disable the sending of direct messages", action="store_true")
parser.add_argument("--config", help="Specify which configuration file to use. It must be a JSON file.",
                    nargs=1, metavar="config_file")
parser.add_argument("--database", help="Specify which SQLite .db file to use", nargs=1, metavar="database_file")
args = parser.parse_args()

# Setup configuration---------------------------------------------------------------------------------------------------
logging_config.set_logging_config(log_file_name)

# Config file
if args.config:
    if os.path.isfile(args.config[0]):
        config_file_name = args.config[0]
    else:
        logging.critical("Incorrect argument: \"{}\" is not a file or does not exist.".format(args.config[0]))
        quit(1)
config = ConfigFileParser(config_file_name)

# Twitter API
try:
    twitter_api = TwitterApi(config.get_twitter_api_credentials())
except KeyError as e:
    logging.critical(e.args[0])
    raise
if twitter_api.verify_credentials() is None:
    logging.critical("The Twitter API credentials in {} are not valid. Twitter Supervisor can not query the Twitter "
                     "API and work properly without correct credentials.".format(config.config_file_name))
    quit(2)

# Database
database = None
try:
    database = Database(config.get_database_credentials())
except KeyError as e:
    logging.critical(e.args[0])
    raise

logging.info("Configuration loaded from: {}".format(config.config_file_name))
logging.info("Data saved in: {}".format(database.database_name))

# Main function---------------------------------------------------------------------------------------------------------
logging.info('Twitter Supervisor launched!')

users = database.get_users()

for user_id in users:

    # Retrieve the previous followers set
    previous_followers = database.get_previous_followers_set(user_id)
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
        messaging.announce_follow_event(True, new_followers, user_id)
        messaging.announce_follow_event(False, traitors, user_id)

    # Save the followers set in DB if there is change
    if len(new_followers) == 0 and len(traitors) == 0:
        logging.info("\"[...] nihil novi sub sole.\" - Ecclesiastes 1:9")
    else:
        database.update_followers_table(user_id, new_followers, traitors)

logging.info("Twitter Supervisor ran successfully!")
