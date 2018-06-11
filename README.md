# no u bot
This is a Twitter bot that replies with some variant of "no u" to any reply that contains "no u".

## How to set up:
### 1. Install the tweepy dependancy for python
``
pip install -r "requirements.txt"
``
### 2. Add your API keys
Put them in a file called
``
credentials.py
``
in the root of the project with the following contents:
```
#API KEYS - Fill these in from Twitter. 
CONSUMER_KEY = '<your consumer key>'
CONSUMER_SECRET = 'your consumer secret>'

ACCESS_KEY = '<your app-specific access key>'
ACCESS_SECRET = '<your app-specific access secret'
USER_HANDLE = "<@your-twitter-username>"
```
### 3. Run it
In the root of the project, use the command
``
python3 no_u_bot.py
``
(it may also work with python 2.7)
