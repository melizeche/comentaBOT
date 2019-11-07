#!/usr/bin/env python3
import json
import time
import tweepy

from apscheduler.schedulers.background import BackgroundScheduler

from lib_comment import singleComment, singleCommentSeed, logError
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, USERNAME_STRING


class TwitterAPI:

    def __init__(self):
        listener = StListener()
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.stream = tweepy.Stream(auth, listener)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        try:
            print(message[:200])
            self.api.update_status(status=message[:200])
        except Exception as err:
            msg = "Tweet Error: {0}".format(err)
            print(msg)
            logError(msg)

    def reply(self, message, reply_id):
        try:
            print(message[:200])
            self.api.update_status(
                status=message[:200], in_reply_to_status_id=reply_id)
        except Exception as err:
            msg = "Reply Error: {0}".format(err)
            print(msg)
            logError(msg)


class StListener(tweepy.streaming.StreamListener):

    def on_data(self, data):
        parsed_tweet = json.loads(data)
        print(parsed_tweet)
        text = parsed_tweet['text'].split()
        user = "@" + parsed_tweet['user']['screen_name']
        if text[0].upper() == USERNAME_STRING.upper():
            if len(text)>1:
                replyTweetSeed(text[1:4], parsed_tweet['id'], user)
            else:
                replyTweet(parsed_tweet['id'], user)
        return True

    def on_error(self, status):
        logError(status)
        print(status)


def singleTweet():
    tweet = singleComment()
    twitter.tweet(tweet)


def singleTweetSeed(seed):
    tweet = singleCommentSeed(seed)
    twitter.tweet(tweet)

def replyTweet(reply_id, user):
    tweet = "%s %s" % (user, singleComment())
    twitter.reply(tweet, reply_id)

def replyTweetSeed(seed, reply_id, user):
    tweet = "%s %s" % (user, singleCommentSeed(' '.join(seed))) 
    twitter.reply(tweet, reply_id)


twitter = TwitterAPI()

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(singleTweet, 'interval', hours=2)
    scheduler.start()
    twitter.stream.filter(track=[USERNAME_STRING], async=True)
    singleTweet()
    # Testing changes
    # try:
    #     # This is here to simulate application activity (which keeps the main thread alive).
    #     while True:
    #         time.sleep(2)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
