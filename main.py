import tweepy
import sqlite3

import config

print("---- Twitter Supervisor ----")

# API configuration
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

# GET current followers list
followers_ids = api.followers_ids(config.username)
followers_number = len(followers_ids)
print("Current number of followers: %s" %followers_number)

# Persistence configuration
connection = sqlite3.connect('followers.db')
c = connection.cursor()

# Get previous followers list
c.execute('CREATE TABLE IF NOT EXISTS followers (id real)')
connection.commit()
c.execute('SELECT * FROM followers')
previous_followers = c.fetchall()
print("Previous number of followers: %s" %len(previous_followers))

# TODO: Comparaison des deux listes
#try:
#    last_follower = api.get_user(id = followers_ids[0])
#    name = last_follower.name
#    print("Dernier follower: ?" ?name)
#except tweepy.TweepError:
#    print(TweepError.response.text)

# Refresh database content
c.execute('DELETE FROM followers')
def id_generator():
    for id in followers_ids:
        yield (id,)
c.executemany("INSERT INTO followers(id) VALUES(?)", id_generator())
connection.commit()
connection.close()

print("---- Fin du programme ----")
