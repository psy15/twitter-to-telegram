import telegram
import GetOldTweets3 as got
import os
import logging
import sys

from time import sleep

log = logging.getLogger('__name__')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s- %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

if 'TOKEN1' not in os.environ:
    raise RuntimeError("Put telegram bot token in TOKEN1 env var")

if 'USERNAME1' not in os.environ:
    raise RuntimeError("Put twitter username name in USERNAME1 env var")

if 'CHANNEL1' not in os.environ:
    raise RuntimeError("Put channel name in CHANNEL1 env var")

TOKEN1 = os.environ['TOKEN1']
USERNAME1 = os.environ['USERNAME1']
CHANNEL1 = os.environ['CHANNEL1']


def read_last_tweet_id():
    try:
        with open('last_tweet.txt', 'r') as file:
            return file.read().strip()
    except:
        return None


def write_last_tweet_id(tweet_id):
    try:
        with open('last_tweet.txt', 'w') as file:
            file.write(tweet_id)
    except:
        log.exception("Error writing tweet ID")


last_tweet_id = read_last_tweet_id()
start_posting = False

if not last_tweet_id:
    log.info(
        "Last posted tweet(id) not found, posting tweets from the beginning now.")
    start_posting = True
else:
    log.info("Last posted tweet id is {}".format(last_tweet_id))


# Creation of query object
tweetCriteria = got.manager.TweetCriteria().setUsername(USERNAME1)\
    .setMaxTweets(100)
# Creation of list that contains all tweets
tweets = got.manager.TweetManager.getTweets(tweetCriteria)

user_tweets = [tweet.text for tweet in tweets]
tweet_links = [tweet.permalink for tweet in tweets]
tweet_ids = [tweet.id for tweet in tweets]
tweets_n_links = dict(zip(tweet_ids, zip(user_tweets, tweet_links)))

bot = telegram.Bot(token=TOKEN1)


message_template = "<b>{title}</b> <a href='{link}'>{lin}</a>"

for i, j in reversed(list(tweets_n_links.items())):
    try:
        if not start_posting:
            log.info(
                "Skipping {} - last sent tweet not yet found".format(j[1]))
            if i == last_tweet_id:
                start_posting = True
            continue

        message = message_template.format(link=j[1], lin='[link]', title=j[0])
        log.info("Posting tweet having url: {}".format(j[1]))
        bot.sendMessage(chat_id=CHANNEL1,
                        parse_mode=telegram.ParseMode.HTML, text=message, disable_web_page_preview=True)
        write_last_tweet_id(i)
        sleep(50)
    except Exception as e:
        log.exception("Error parsing {}".format(j[1]))
