import logging
from typing import List

import peony
from faust.cli import option
from peony import PeonyClient

from src.app import app, hashtags_topic
from src.settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

logger = logging.getLogger(__name__)


@app.command(option("--track", type=str, help="List of words in CSV format to filter stream of tweets", required=True))
async def hashtags_events_generator(self, track: str):
    """
    Generate Kafka events for each hashtag found in tweets matching with the track used to filter the stream.
    """
    logger.info(f"Searching tweets with track: {track}")

    client = _get_twitter_client()
    req = client.stream.statuses.filter.post(track=track)

    async with req as stream:
        async for tweet in stream:
            tweet_hashtags = _get_hashtags_from_tweet(tweet=tweet)
            await _produce_events_for_hashtags(hashtags=tweet_hashtags)


def _get_twitter_client() -> PeonyClient:
    creds = dict(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    return PeonyClient(**creds)


def _get_hashtags_from_tweet(tweet) -> List[str]:
    tweet_hashtags = []

    if peony.events.tweet(tweet):
        tweet_hashtags = tweet['entities']['hashtags']

    return tweet_hashtags


async def _produce_events_for_hashtags(hashtags: List[str]) -> None:
    for tweet_hashtag in hashtags:
        logger.info(f'Sending event for hashtag: {tweet_hashtag["text"].lower()}')
        await hashtags_topic.send(value=tweet_hashtag["text"].lower())
