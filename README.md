# Twitter Supervisor
> "I made this program to learn about Python and to know who stop following me on Twitter." - Quentin JODER 

Twitter Supervisor informs you (via direct message) when someone follows or unfollows you.

Additional features might be added in the (near) future: keep in database the data of the "betrayals", trends detection in the friends
(people you are following) tweets...

## Requirements
* **Python 3.5 or 3.6** (There are problems with 3.7 and older versions have not been tested) and **pip**
* **Having a (at least free) Twitter developer account** (https://developer.twitter.com/en/apply-for-access), to get the key,
the token and their secrets, which are all required to access the Twitter API.

## Installation
* Clone the project repository on your machine.
* Run `pip install -Ur requirements.txt`
* Create a `config.json` file in the project directory, where you will put the API keys, the id of the account you want to supervise, and the name of the SQLite database file where the app data will be stored.
It should look like this:

    ```json
    {
      "twitter_api": {
        "username": "@aTwitterUserName",
        "consumer_key": "...",
        "consumer_secret": "...",
        "access_token": "...",
        "access_token_secret": "..."
      },
      "database_file": "followers.db"
    }
    ```

## Tests
in the project directory, run: 
```bash
$ pytest tests
``` 

## How to use it?
Run `$ python main.py`(Windows) or `$ python3 main.py`(Linux):
* the first time it will only create a `followers.db` SQLite database (containing the IDs of your followers) and a `.log` file.
* Then, each time this command is run, it will send a direct message to the specified Twitter account (from itself) to tell you who are the followers you have gained or lost in the meantime.

> Pro-tip: the names of the new followers & unfollowers are in the log file too.

If you wish to automate this operation, you can, for example, create a scheduled job on a Linux server with **cron**:
* edit the crontab file of a user with the command `crontab -e`
* if you want to check for new followers/unfollowers each day at 7:00 a.m, insert:
<br/>`0 7 * * * cd [path to the parent directory of "Twitter-Supervisor"]/Twitter-Supervisor && python3 main.py`
<br/>(`0 7 * * *` is the schedule time, https://crontab.guru/ can help you to define it. The rest of the entry is the 
command cron will run)
* save and close the editor with `Ctrl+X`and then `Y`(nano) or `:wq`(vim), and it is done !

For more information about cron, the syntax of the crontab files, nano or vim... ask your favorite search engine !
