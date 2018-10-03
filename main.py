import logging

import database
import twitter_api

# Logging configuration---------------------------------------------------------
# logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='twitter_supervisor.log')
# logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Function to "publish" the name of the new followers & unfollowers-------------
def publishUsernames(following, user_ids):
    if following:
        message = "%s (@%s) follows you now."
    else:
        message = "%s (@%s) unfollowed you."
    for user_id in user_ids:
        user = twitter_api.getUser(user_id)
        message = message % (user.name, user.screen_name)
        twitter_api.sendDirectMessage(message)
        logging.info(message);

# Main function-----------------------------------------------------------------
logging.info('Twitter Supervisor launched!')

# Retrieve the previous followers set
previous_followers = database.getPreviousFollowersSet()
previous_followers_number = len(previous_followers)

# Get the current followers set
current_followers = twitter_api.getFollowersSet()
followers_number = len(current_followers)
logging.info("Current number of followers: %d" % followers_number)

# Comparison of the two sets of followers
if previous_followers_number != 0:
    logging.info("Previous number of followers: %d" % previous_followers_number)
    new_followers = current_followers - previous_followers
    publishUsernames(True, new_followers)
    unfollowers = previous_followers - current_followers
    publishUsernames(False, unfollowers)
# If there are no followers saved in DB, we consider it is the first use
else:
    print("Thank you for using Twitter Supervisor, we are saving your followers\
     for later use of the program...")

# Save the followers set in DB if there is change
if len(new_followers) == 0 and len(unfollowers) == 0:
    logging.info("\"[...] nihil novi sub sole.\" - Ecclesiastes 1:9")
else:
    database.saveFollowersSet(current_followers)

logging.info("Twitter Supervisor ran successfully!")
