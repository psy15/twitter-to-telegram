import telegram
import GetOldTweets3 as got
import os
import logging
import sys

from time import sleep
from datetime import datetime

log = logging.getLogger('__name__')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s- %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

if 'TOKEN1' not in os.environ:
    raise RuntimeError("Put bot token in TOKEN1 env var")

if 'USERNAME1' not in os.environ:
    raise RuntimeError("Put twitter username name in USERNAME1 env var")

if 'CHANNEL1' not in os.environ:
    raise RuntimeError("Put channel name in CHANNEL1 env var")

TOKEN1 = os.environ['TOKEN1']
USERNAME1 = os.environ['USERNAME1']
CHANNEL1 = os.environ['CHANNEL1']


# Creation of query object
tweetCriteria = got.manager.TweetCriteria().setUsername(USERNAME1)\
    .setMaxTweets(1000)
# Creation of list that contains all tweets
tweets = got.manager.TweetManager.getTweets(tweetCriteria)

user_tweets = [tweet.text for tweet in tweets]
tweet_links = [tweet.permalink for tweet in tweets]
tweet_ids = [tweet.id for tweet in tweets]
tweets_n_links = dict(zip(user_tweets, tweet_links))

bot = telegram.Bot(token=TOKEN1)


message_template = "<b>{title}</b> <a href='{link}'>{lin}</a>"
# message_template = "<a> {title}</a> <b href='{link}'>{lin}</b>"
for i, j in reversed(list(tweets_n_links.items())):
    message = message_template.format(link=j, lin='[link]', title=i)
    log.info("Posting {}".format(j))
    bot.sendMessage(chat_id=CHANNEL1,
                    parse_mode=telegram.ParseMode.HTML, text=message, disable_web_page_preview=True)
    # write_last_submission_id(tweet_ids[i])
    sleep(40)
