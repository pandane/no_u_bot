#!/usr/bin/env python
# coding: utf8

import tweepy
import time
import sys
import re
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, USER_HANDLE

import random


class ReplyStreamListener(StreamListener):
    def __init__(self):
        self.wait = 0
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        self.lastTweeted = ""
        self.lastTweetedCount = 0

    def on_status(self, status):
        try:
            # content of responses is randomly chosen from this list:
            tweetResponses = ['no u', 'NO UU', 'NO U',
                              'nO U', 'NO U!!', '\nNO U\nO\n\nU']

            # ignore whitespace and upper/lower cases
            statusText = " ".join(status.text.split()).lower()

            # don't respond to self
            if status.author.screen_name == USER_HANDLE.strip("@"):
                return

            # do not reply to retweets
            if "RT:" in statusText:
                return

            # patterns that trigger a response:
            triggers = ['no u', 'no you']

            # check if reply contains triggers
            triggerNotActivated = True
            for trigger in triggers:
                if trigger in statusText:
                    triggerNotActivated = False

            print("@"+status.author.screen_name+" replied to you:")
            print(status.text)

            # do not reply if there are no triggers present
            if triggerNotActivated:
                return

            # contents of reply message:
            postMsg = '@' + status.author.screen_name + \
                " " + random.choice(tweetResponses)

            # limit to a chain of 5 responses
            if(status.author.screen_name == self.lastTweeted):
                self.lastTweetedCount += 1
            else:
                self.lastTweeted = status.author.screen_name
                self.lastTweetedCount = 0

            if(self.lastTweetedCount > 6):
                return

            # rate limiting detection
            try:
                if(self.wait > 10):
                    return
                elif(self.wait > 0):
                    time.sleep(self.wait)

                # post reply
                print("")
                print("You ("+USER_HANDLE+") replied with:")
                print(postMsg)
                print("")

                self.api.update_status(postMsg, status.id)
                self.wait = 0
            except Exception as rateLimitException:
                self.wait += 1
                print(rateLimitException)
                return

        except Exception as statusAccessException:
            print(statusAccessException)
            return

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = ReplyStreamListener()

    stream = Stream(listener.auth, listener)
    stream.userstream()
