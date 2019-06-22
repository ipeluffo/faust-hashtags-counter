import logging
import os
from typing import Optional

import tweepy
from faust.cli import option

from commands.tweetpy_listeners import LogStreamListener
from src.app import app

logger = logging.getLogger(__name__)


@app.command(
    option("--hash-tag", type=str, help="Hash tag to use to search tweets", required=True)
)
async def tweets_generator(self, hash_tag: str):
    """Print tweets found in real-time filtered by hash-tag"""
    hash_tag = _clean_hash_tag(hash_tag=hash_tag)
    if not hash_tag:
        logger.info('Hash tag is mandatory')
        return

    logger.info(f"Searching tweets with hash tag: {hash_tag}")
    api = _get_twitter_client()
    my_stream = tweepy.Stream(auth=api.auth, listener=LogStreamListener())
    my_stream.filter(track=[hash_tag], is_async=True)


def _clean_hash_tag(hash_tag: str) -> Optional[str]:
    if not hash_tag or len(hash_tag.strip()) < 1:
        return None

    hash_tag = hash_tag.strip()
    hash_tag = hash_tag if hash_tag[0] == '#' else f'#{hash_tag}'
    return hash_tag


def _get_twitter_client() -> tweepy.API:
    CONSUMER_KEY = os.getenv("CONSUMER_KEY", None)
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET", None)
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET", None)

    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth_handler=auth)
    return api
