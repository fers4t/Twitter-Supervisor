import tweepy
import sqlite3

import config

print("---- Twitter Supervisor ----")

# API configuration
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

# GET current followers list
current_followers = set(api.followers_ids(config.username))
followers_number = len(current_followers)
print("Current number of followers: %d" %followers_number)

# Persistence configuration
connection = sqlite3.connect('followers.db')
c = connection.cursor()

# Get previous followers list from DB
c.execute('CREATE TABLE IF NOT EXISTS followers (id integer)')
connection.commit()
c.execute('SELECT * FROM followers')
previous_followers_list = c.fetchall()
previous_followers = set()
for follower in previous_followers_list:
    previous_followers.add(int(follower[0]))
previous_followers_number = len(previous_followers)

# We consider that if there are no followers saved in DB, it is the first use
# of the program by the user
if previous_followers_number != 0:
    print("Previous number of followers: %d" %previous_followers_number)

    # Method to display new followers & unfollowers
    def displayMessageAboutUsers(message, user_ids):
        for user_id in user_ids:
            try:
                user = api.get_user(user_id)
                print(message %(user.name, user.screen_name))
            except tweepy.TweepError:
                print("Erreur: " + TweepError.response.text)

    new_followers = current_followers - previous_followers
    displayMessageAboutUsers("%s (@%s) follows you now.", new_followers)
    unfollowers = previous_followers - current_followers
    displayMessageAboutUsers("%s (@%s) unfollowed you.", unfollowers)
    if len(new_followers) == 0 and len(unfollowers) == 0:
        print("\"Nihil novi sub sole\". - Ecclesiastes 1:9")
else:
    print("Thank you for using Twitter Supervisor, we are saving your followers\
     for later use of the program...")

# Refresh database content
# TODO: Solve the bug preventing to save the last follower
c.execute('DELETE FROM followers')
def id_generator():
    for id in current_followers:
        yield (id,)
c.executemany("INSERT INTO followers(id) VALUES(?)", id_generator())
connection.commit()
connection.close()

print("Twitter Supervisor ran successfully!")
