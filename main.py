import tweepy
import config

print("---- Twitter Supervisor ----")
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

followers_ids = api.followers_ids(config.username)
followers_number = len(followers_ids)
print("Nombre de followers: %s" % followers_number)
last_follower = api.get_user(id = followers_ids[0])
name = last_follower.name
print("Dernier follower: %s" %name)
print("---- Fin du programme ----")
