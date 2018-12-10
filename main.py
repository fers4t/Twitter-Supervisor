# External dependencies
import argparse
import logging
# Custom dependencies
import config
import logging_config
from twittersupervisor import TwitterApi, Database, Messaging


# Command line parsing
parser = argparse.ArgumentParser()
parser.add_argument("--quiet", help="Disable the sending of direct messages", action="store_true")
args = parser.parse_args()

# Setup config
# TODO Retrieve config data from:
#  - a yaml/json/ini config file (especially for Twitter API credentials)
#  - command line arguments (log and database files)
#  - default values
#  If the Twitter API credentials are not found, handle this error case
logging_config.set_logging_config("twitter_supervisor.log")
twitter_api = TwitterApi(config.USERNAME, config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_TOKEN,
                         config.ACCESS_TOKEN_SECRET)
database = Database("followers.db")

# Main function---------------------------------------------------------------------------------------------------------
logging.info('Twitter Supervisor launched!')

# Retrieve the previous followers set
previous_followers = database.get_previous_followers_set()
previous_followers_number = len(previous_followers)

# Get the current followers set
current_followers = twitter_api.get_followers_set()
# TODO Handle cases:
#  1) the user really doesn't have any follower :(
#  2) the API is unreachable/ doesn't reply
if current_followers is None:
    quit()
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
