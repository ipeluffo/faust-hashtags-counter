import logging

import tweepy
from tweepy.models import Status

logger = logging.getLogger(__name__)


class LogStreamListener(tweepy.StreamListener):

    def on_status(self, status: Status):
        if status.truncated:
            logger.info(status.extended_tweet['full_text'])
            logger.info([x['text'] for x in status.extended_tweet['entities']['hashtags']])
        else:
            logger.info(status.text)
            logger.info([x['text'] for x in status.entities['hashtags']])
