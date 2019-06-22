# Faust tweets counter
Sample Faust project to process tweets in real-time

## Part 1
In this part, we'll create a [custom faust CLI command](https://faust.readthedocs.io/en/latest/userguide/tasks.html#cli-commands) to process a stream of tweets using a specific hash-tag.

What we're doing:
* Writing a Faust custom CLI command
* Integrating [tweepy](https://www.tweepy.org) to process Twitter stream

In this part, we're just printing on console the tweets content and hash tags. In the next section we'll send tweets to a Kafka topic to be processed by Faust workers.

### Requirements
* Python 3.6+
* Twitter developer account

### Setup Twitter secrets
1. Make copy of `.env.example` file and rename it as `.env`
2. Set values from your developer account

### Install dependencies
```bash
pip install -U pipenv
pipenv sync 
```

To use dependencies for development:
```bash
pipenv sync --dev
```

### How to run the custom command?
From project's folder:
```bash
pipenv run faust -A commands.commands -l info tweets_generator --hash-tag your_hash_tag
```

### Get command help
```bash
pipenv run faust -A commands.commands -l info tweets_generator --help
```

### Output example:
```
➜ pipenv run faust -A commands.commands -l info tweets_generator --hash-tag python
Loading .env environment variables…
[2019-06-22 18:30:35,440: INFO]: [^Worker]: Starting...
[2019-06-22 18:30:35,441: INFO]: Searching tweets with hash tag: #python
[2019-06-22 18:30:35,445: INFO]: [^Worker]: Stopping...
[2019-06-22 18:30:35,446: INFO]: [^Worker]: Gathering service tasks...
[2019-06-22 18:30:35,446: INFO]: [^Worker]: Gathering all futures...
[2019-06-22 18:30:36,449: INFO]: [^Worker]: Closing event loop
[2019-06-22 18:30:40,786: INFO]: RT @FullstackDevJS: An easy approach to contribute to Open Source Project #Fullstack #Javascript #Angular #React #Python https://t.co/hKQpS…
[2019-06-22 18:30:40,786: INFO]: ['Fullstack', 'Javascript', 'Angular', 'React', 'Python']
[2019-06-22 18:30:46,279: INFO]: 2019-06-22 18:30:03
-Download (Mb/s): 5.62
-Upload (Mb/s): 10.80
-Ping (ms): 56.58

I pay for 55Mb/s down with broadband. The threshold for this tweet was 15Mb/s.
#Python #RaspberryPi #SpeedTest
[2019-06-22 18:30:46,279: INFO]: ['Python', 'RaspberryPi', 'SpeedTest']
```
