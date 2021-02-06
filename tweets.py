import telegram
import GetOldTweets3 as got
import os
import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import github

from time import sleep, time

PORT = int(os.environ.get('PORT', 5000))

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = False

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s- %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

if ('TOKEN' or 'GTOKEN' or 'CHANNEL' or 'USERNAME') not in os.environ:
    raise RuntimeError("env/config vars missing!")


TOKEN = os.environ.get('TOKEN', None)
CHANNEL = os.environ.get('CHANNEL', None)
GTOKEN = os.environ.get('GTOKEN', None)
USERNAME = os.environ.get('USERNAME', None)
GISTID = os.environ.get('GISTID', None)

gh = github.Github(GTOKEN)
gist = gh.get_gist(GISTID)


def start(update, context):
    update.message.reply_text('Hey there!')


def error(update, context):
    log.warning('Update "%s" caused error "%s"', update, context.error)


def read_last_tweet_id():
    try:
        file = gist.files['last_post'].content
        return file.strip()
    except:
        log.exception("Error reading tweet ID")


def write_last_tweet_id(tweet_id):
    try:
        gist.edit(
            description="using for heroku",
            files={"last_post": github.InputFileContent(content=tweet_id)},
        )
    except:
        log.exception("Error writing tweet ID")


def post_tweets():
    last_tweet_id = read_last_tweet_id()
    start_posting = False

    if not last_tweet_id:
        log.info(
            "Last posted tweet(id) not found, posting tweets from the beginning now.")
        start_posting = True
    else:
        log.info("Last posted tweet id is {}".format(last_tweet_id))

    tweetCriteria = got.manager.TweetCriteria().setUsername(USERNAME)\
        .setMaxTweets(50)

    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    user_tweets = [tweet.text for tweet in tweets]
    tweet_links = [tweet.permalink for tweet in tweets]
    tweet_ids = [tweet.id for tweet in tweets]
    tweets_n_links = dict(zip(tweet_ids, zip(user_tweets, tweet_links)))

    bot = telegram.Bot(token=TOKEN)

    message_template = "<b>{title}</b> <a href='{link}'>{lin}</a>"

    for i, j in reversed(list(tweets_n_links.items())):
        try:
            if not start_posting:
                log.info(
                    "Skipping {} - last sent tweet not yet found".format(j[1]))
                if i == last_tweet_id:
                    start_posting = True
                continue

            message = message_template.format(
                link=j[1], lin='[link]', title=j[0])
            log.info("Posting tweet having url: {}".format(j[1]))
            bot.sendMessage(chat_id=CHANNEL,
                            parse_mode=telegram.ParseMode.HTML, text=message, disable_web_page_preview=True)
            write_last_tweet_id(i)
            sleep(10)
        except Exception:
            log.exception("Error parsing {}".format(j[1]))


def main():

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(
        'https://app-name.herokuapp.com/' + TOKEN)

    post_tweets()


if __name__ == '__main__':
    main()
