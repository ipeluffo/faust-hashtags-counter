from faust.app import App

from src.settings import BOOTSTRAP_SERVERS

app = App(
    id='hashtags_counter',
    broker=f'kafka://{BOOTSTRAP_SERVERS}',
    store='memory://',
    autodiscover=True,
    origin='src',
)

hashtags_topic = app.topic('hashtags', value_type=str, internal=True)

hashtags_counts_table = app.Table('hashtags_counts', default=int)
