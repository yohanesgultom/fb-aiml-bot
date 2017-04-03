# fb-aiml-bot

Facebook messenger bot using AIML (parsed using PyAIML https://github.com/creatorrr/pyAIML) using data from https://github.com/mmellott/aiml-fb-chat

**Requirements**

```
pip install Flask
pip install requests
pip install requests[security]
```

additionally, for testing:

```
pip install responses
```

**Configuration**

A config file named `config` need to be created in the same directory as `server.py`. Example:

```
[aimlbot]
# bot name (affecting question such as 'What is your name?')
botname = aimlbot
# facebook page token
fb_page_token = XXXXXXXXXXXXXXXXXXXXXXXX
# randomly generated value for secretive facebook api web-hook
secret = XXXXXXXXXXXXXXXXXXXXXXXX
# randomly generated value for facebook api web-hook verification
verify_token = XXXXXXXXXXXXXXXXXXXXXXXX
# facebook api url
fb_api_url = https://graph.facebook.com/v2.6/me/messages?access_token=

[botprofile]
name = aimlbot
gender = Male

```
Possible `[botprofile]` are:
```
birthday
birthplace
boyfriend
favoriteband
favoritebook
favoritecolor
favoritefood
friends
gender
girlfriend
kindmusic
location
looklike
master
name
question
sign
talkabout
wear
```

>

**Usage**

Running Flask bot server as standalone (dev or test):

```
python server.py
```

To try chatting with AIML bot in CLI:

```
python chat.py
```

To run unit tests using `pytest`:

```
pytest
```


For production, consider using UWSGI + web server (eg. Nginx) (reference below)

**Reference**

* Setting up UWSGI + Flask http://flask.pocoo.org/docs/0.12/deploying/uwsgi/
* Setting up UWSGI Emperor (UWSGI as service) + Nginx https://kradalby.no/uwsgi-and-nginx-on-debian-wheezy.html
