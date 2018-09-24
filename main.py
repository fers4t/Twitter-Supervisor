import logging
import sqlite3
import tweepy

import config

# Logging configuration---------------------------------------------------------
# logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='twitter_supervisor.log')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set the output format on the console
formatter = logging.Formatter('%(levelname)-8s: %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logging.info('Twitter Supervisor launched!')

# Retrieve the previous followers list------------------------------------------
# Persistence configuration
connection = sqlite3.connect('followers.db')
c = connection.cursor()

# Query the database
c.execute('CREATE TABLE IF NOT EXISTS followers (id integer)')
connection.commit()
c.execute('SELECT * FROM followers')
previous_followers_list = c.fetchall()
previous_followers = set()
for follower in previous_followers_list:
    previous_followers.add(int(follower[0]))
previous_followers_number = len(previous_followers)

# Query the Twitter API---------------------------------------------------------
# API configuration
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

# GET current followers list
current_followers = set(api.followers_ids(config.username))
followers_number = len(current_followers)
logging.info("Current number of followers: %d" % followers_number)

# Comparison of the two sets of followers---------------------------------------
if previous_followers_number != 0:
    logging.info("Previous number of followers: %d" % previous_followers_number)

    # Method to display new followers & unfollowers
    def displayMessageAboutUsers(message, user_ids):
        for user_id in user_ids:
            try:
                user = api.get_user(user_id)
                logging.info(message %(user.name, user.screen_name))
            except tweepy.TweepError as error :
                logging.error("An error happened when we tried to find user\
                 %d: %s" % (user_id, error.reason))

    new_followers = current_followers - previous_followers
    displayMessageAboutUsers("%s (@%s) follows you now.", new_followers)
    unfollowers = previous_followers - current_followers
    displayMessageAboutUsers("%s (@%s) unfollowed you.", unfollowers)
    if len(new_followers) == 0 and len(unfollowers) == 0:
        logging.info("\"[...] nihil novi sub sole.\" - Ecclesiastes 1:9")

# If there are no followers saved in DB, we consider it is the first use
else:
    print("Thank you for using Twitter Supervisor, we are saving your followers\
     for later use of the program...")

# Refresh database content------------------------------------------------------
# TODO: Solve the bug preventing to save the last follower
c.execute('DELETE FROM followers')
def id_generator():
    for id in current_followers:
        yield (id,)
c.executemany("INSERT INTO followers(id) VALUES(?)", id_generator())
connection.commit()
connection.close()

logging.info("Twitter Supervisor ran successfully!")
