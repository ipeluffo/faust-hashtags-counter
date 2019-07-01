# Hashtags counter with Faust
Sample Faust project to process tweets in real-time and count hashtags.

## What are we building?

### 1. Custom Faust CLI command
A [custom faust CLI command](https://faust.readthedocs.io/en/latest/userguide/tasks.html#cli-commands) is responsible for filtering a stream of tweets using a list of words in CSV format.

More information about Twitter API `track` filter: [https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html](https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html).

For this, the command is integrated with [peony-twitter](https://github.com/odrling/peony-twitter) to process the [Twitter stream](https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter.html).

Finally, the command will create one event for each hashtag found in tweets returned by the Twitter stream.

### 2. Faust agent to process events
The agent will process all events and store the hashtags counters in a [tumbling window table](https://faust.readthedocs.io/en/latest/userguide/tables.html#TumblingWindow).

### 3. Faust view
This project will expose a few Faust views:
1. Get hashtag count
2. Get hashtag [state for current window](https://faust.readthedocs.io/en/latest/userguide/tables.html#how-to)
3. Get all hashtags (expensive view)

## Requirements
* Python 3.6+
* `pipenv`: https://docs.pipenv.org/en/latest/
* Twitter developer account: https://developer.twitter.com/en.html

### Setup Twitter secrets
1. Make copy of `.env.example` file and rename it as `.env`
2. Set values from your developer account

### Install dependencies
```bash
pip install -U pipenv
pipenv sync 
```

To install dependencies for development:
```bash
pipenv sync --dev
```

## How to run the project
### Set all environment variables
Check all env vars defined in the `.env` file and set the corresponding values.

__Note__:
* Kafka connection string is the list of brokers with the port separated by semicolon.

### Have a Kafka instance running
You can use your own cluster or use one of the docker compose file provided in the `docker` folder.

#### Running using Docker Compose
From `docker` folder:
```bash
docker-compose up
```

This will run both Zookeeper and Kafka using the default ports `2181` and `9092`.

If you want to store the data, from `docker` folder, run:
```bash
docker-compose -f docker-compose-with-storage.yml up
```

#### Stopping containers
Just stop containers running pressing `CTRL+C`, or from another window run:
```bash
docker-compose stop
```

### Run CLI command
From project's folder:
```bash
pipenv run faust -A commands.commands -l info hashtags_events_generator --hashtags hashtag1,hashtag2
```

#### Get command help
```bash
pipenv run faust -A commands.commands -l info hashtags_events_generator --help
```

### Run Faust worker
In a different terminal:
```bash
pipenv run faust -A src.app worker -l info
```

__Important__:
1. This will expose the views on the default port `6066`
2. The worker will store data in the default folder
