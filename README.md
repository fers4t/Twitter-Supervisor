# Twitter Supervisor
> My first goal in this project is to learn about Python and the Twitter API! - The developer

## What is Twitter Supervisor?
Twitter Supervisor provides small but useful functionalities for a Twitter user:
* Detection of unfollowers (development ongoing)
* ...

## Requirements
* Python 3.6 (There are problems with 3.7 and older versions have not been tested)
* Tweepy (https://github.com/tweepy/tweepy): you should normaly only need to execute `pip install tweepy` to install it on your PC.
* Having a (at least free) Twitter developer account (https://developer.twitter.com/en/apply-for-access), to get the key, 
the token and their secrets which are required to access the Twitter API. (One of my objective is to quickly get rid of this requirement)

## Installation
* Clone the project repository on your machine.
* Create a `config.py` file in the project directory, where you will put the API keys and the id of the account you want to supervise. 
It should look like this:
	
	```
	# Key, token & secrets
	consumer_key = "..."
	consumer_secret = "..."
	access_token = "..."
	access_token_secret = "..."```

	# user
	username = "@username"
	```

## How to use it?
Run `python main.py` in a shell in the project directory:
* the first time it will only create a `followers.db` SQLite database containing the IDs of your followers.
* Then, each time you run this command, it will tell you who are the followers you have gained or lost in the meantime. 
