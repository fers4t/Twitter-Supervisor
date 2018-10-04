# Twitter Supervisor
> The main purpose of this project is enable me to learn about Python and the Twitter API! - The developer

## What is Twitter Supervisor?
The goal of Twitter Supervisor is to provide small but useful functionalities for any Twitter user:
* Detection of unfollowers: it sends a direct message to your account to inform you if someone unfollow you.
* [The development of other functionalities is ongoing]

## Requirements
* **Python 3.5 or 3.6** (There are problems with 3.7 and older versions have not been tested) and **pip**
* **python-twitter** (https://github.com/bear/python-twitter): Twitter Supervisor uses this wrapper to query the Twitter API. Run `pip install python-twitter` to install it on your PC. You need at least the 3.5 version, because it is the first one adapted to the changes made in September 2018 to the API.
* **Having a (at least free) Twitter developer account** (https://developer.twitter.com/en/apply-for-access), to get the key,
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
	username = "@yourusername"
	```

## How to use it?
Run `python main.py`(Windows) or `python3 main.py`(Linux) in a shell in the project directory:
* the first time it will only create a `followers.db` SQLite database (containing the IDs of your followers) and a `.log` file.
* Then, each time this command is run, it will send a direct message to the specified Twitter account (from itself) to tell you who are the followers you have gained or lost in the meantime.

> Pro-tip: the name of the new followers & unfollowers is in the log file too.

If you wish to automate this operation, you can, for example, create a scheduled job on a Linux server with **cron**:
* edit the crontab file of a user with the command `crontab -e`
* if you want to check for new followers/unfollowers each day at 7:00 a.m, insert:
<br/>`0 7 * * * cd [path to the parent directory of "Twitter-Supervisor"]/Twitter-Supervisor && python3 main.py`
<br/>(`0 7 * * *` is the schedule time, https://crontab.guru/ can help you to define it. The rest of the entry is the command cron will run)
* save and close the editor with `Ctrl+X`and then `Y`(nano) or `:wq`(vim), and it is done !

For more information about cron, the syntax of the crontab files, nano or vim... ask your favorite search engine !
