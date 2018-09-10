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
print("Current number of followers: %s" %followers_number)

# Persistence configuration
connection = sqlite3.connect('followers.db')
c = connection.cursor()

# Get previous followers list
c.execute('CREATE TABLE IF NOT EXISTS followers (id integer)')
connection.commit()
c.execute('SELECT * FROM followers')
previous_followers_list = c.fetchall()
previous_followers = set()
for follower in previous_followers_list:
    previous_followers.add(int(follower[0]))
print("Previous number of followers: %s" %len(previous_followers))

# Display new followers & unfollowers
def displayMessageAboutUsers(message, user_ids):
    for user_id in user_ids:
        try:
            user = api.get_user(user_id)
            print(message %user.name)
        except tweepy.TweepError:
            print(TweepError.response.text)

new_followers = current_followers - previous_followers
displayMessageAboutUsers("%s vous suit désormais.", new_followers)
unfollowers = previous_followers - current_followers
displayMessageAboutUsers("%s a cessé de vous suivre.", unfollowers)

# Refresh database content
# TODO: Solve the bug preventing to save the last follower
c.execute('DELETE FROM followers')
def id_generator():
    for id in current_followers:
        yield (id,)
c.executemany("INSERT INTO followers(id) VALUES(?)", id_generator())
connection.commit()
connection.close()

print("---- Fin du programme ----")
