# twitter-to-telegram

This script uses GetOldTweets3 library to get new tweets and post it to a Telegram channel.

## Config

* Set the following env vars:
  * `USERNAME` - twitter username
  * `TOKEN` - telegram bot token
  * `CHANNEL` - telegram channel name (the bot has to be added as an administrator)
  * `GTOKEN` - github access token 
  * `GISTID` -  github gist id
  
  
* Run `python3 tweets.py`

## Notes

The last posted tweet id is stored in a gist file, so the script will read the last tweet id from this gist.
if this file exists, then the script will skip all the tweets that have been posted earlier 
until this ID is found. else, it will post the tweets from the beginning and store the latest to this file.
