from src.app import app, hashtags_topic, hashtags_counts_table


@app.agent(hashtags_topic)
async def hashtags_counter(hashtags) -> None:
    async for hashtag in hashtags:  # type: str
        hashtags_counts_table[hashtag] += 1
