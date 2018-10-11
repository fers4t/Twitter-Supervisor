import logging

import logging_config
import database
import twitter_api

# Function to "publish" the name of the new followers & unfollowers-------------
def publish_usernames(following, user_ids):
    if following:
        message = '{0} (@{1}) follows you now.'
    else:
        message = '{0} (@{1}) unfollowed you.'
    for user_id in user_ids:
        user = twitter_api.get_user(user_id)
        if user is not None:
            message = message.format(user.name, user.screen_name)
            twitter_api.send_direct_message(message)
            logging.info(message)

# Main function-----------------------------------------------------------------
logging.info('Twitter Supervisor launched!')

# Retrieve the previous followers set
previous_followers = database.get_previous_followers_set()
previous_followers_number = len(previous_followers)

# Get the current followers set
current_followers = twitter_api.get_followers_set()
if current_followers is None:
    quit()
followers_number = len(current_followers)
logging.info("Current number of followers: %d" % followers_number)

# Comparison of the two sets of followers
new_followers = current_followers - previous_followers
unfollowers = previous_followers - current_followers

if previous_followers_number != 0:
    logging.info("Previous number of followers: %d" % previous_followers_number)
    publish_usernames(True, new_followers)
    publish_usernames(False, unfollowers)
# If there are no followers saved in DB, we consider it is the first use
else:
    print("Thank you for using Twitter Supervisor, we are saving your followers\
     for later use of the program...")

# Save the followers set in DB if there is change
if len(new_followers) == 0 and len(unfollowers) == 0:
    logging.info("\"[...] nihil novi sub sole.\" - Ecclesiastes 1:9")
else:
    database.save_followers_set(current_followers)

logging.info("Twitter Supervisor ran successfully!")
