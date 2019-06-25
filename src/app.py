from datetime import timedelta

from faust.app import App
from src.settings import BOOTSTRAP_SERVERS

app = App(
    id='tweets_counter',
    broker=f'kafka://{BOOTSTRAP_SERVERS}',
    store='memory://',
    autodiscover=True,
    origin='src',
)

hashtags_topic = app.topic('hashtags', value_type=bytes)

hashtags_counts_table = app.Table('hashtags_counts').tumbling(size=timedelta(seconds=5))
