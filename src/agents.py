import logging

from src.app import app, hashtags_counts_table, hashtags_topic

logger = logging.getLogger(__name__)


@app.agent(hashtags_topic)
async def hashtags_counter(hashtags) -> None:
    async for hashtag in hashtags:  # type: str
        logger.info(f"Processing hashtag: {hashtag}...")
        hashtags_counts_table[hashtag] += 1
