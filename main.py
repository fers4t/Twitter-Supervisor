import tweepy
import config

print("---- Twitter Supervisor ----")
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)

followers_ids = api.followers_ids("@quent1gentil")
followers_number = len(followers_ids)
print("Nombre de followers: %s" % followers_number)
print("Premier follower: %s" %followers_ids[0])
print("---- Fin du programme ----")
