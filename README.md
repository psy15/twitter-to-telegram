# twitter-to-telegram

This script uses GetOldTweets3 library to get new tweets and post it to a Telegram channel.

## Config

* Set the following env vars:
  * `USERNAME` - twitter username
  * `TOKEN` - telegram bot token
  * `CHANNEL` - telegram channel name (the bot has to be added as an administrator)
  
* Run `python3 tweets.py`

## Notes

The last sent tweet id is being stored in `last_tweet.txt` file, so
if this file exists, then the bot will skip all the tweets that have been earlier 
until this ID is found. else, it will post the tweets from the beginning.
