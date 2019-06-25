import logging
from typing import Optional

import peony
from faust.cli import option
from peony import PeonyClient

from src.app import app, hashtags_topic
from src.settings import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN_SECRET, ACCESS_TOKEN

logger = logging.getLogger(__name__)


@app.command(
    option("--hashtags", type=str, help="CSV list of hashtags filter stream of tweets", required=True)
)
async def hashtags_events_generator(self, hashtags: str):
    """
    Generate Kafka events for each hashtag found in tweets matching with the hashtags
    used to filter the stream.
    """
    hashtags = _clean_hashtag(hashtags=hashtags)

    logger.info(f"Searching tweets with hashtags: {hashtags}")

    client = _get_twitter_client()
    req = client.stream.statuses.filter.post(track=hashtags)

    async with req as stream:
        async for tweet in stream:
            if peony.events.tweet(tweet):
                tweet_hashtags = tweet['entities']['hashtags']
                for tweet_hashtag in tweet_hashtags:
                    logger.info(f'Sending event for hashtag: {tweet_hashtag["text"].lower()}')
                    await hashtags_topic.send(value=tweet_hashtag["text"].lower())


def _clean_hashtag(hashtags: str) -> Optional[str]:
    if not hashtags or len(hashtags.strip()) < 1:
        return None

    return ','.join(
        [
            hashtag.strip().lower() if hashtag[0] == '#' else f'#{hashtag.strip().lower()}'
            for hashtag in hashtags.split(',')
        ]
    )


def _get_twitter_client() -> PeonyClient:
    creds = dict(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    return PeonyClient(**creds)
