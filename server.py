import ConfigParser
import requests
import aiml
import json
from flask import (Flask, request)
from pprint import pprint

config = ConfigParser.RawConfigParser()
config.read('config')

fb_page_token = 'fb_page_token'
fb_api_url = 'fb_api_url'
secret = 'secret'
verify_token = 'verify_token'
post_message_url = 'post_message_url'

# read config
config_section = 'aimlbot'
if config.has_section(config_section):
    fb_page_token = config.get(config_section, 'fb_page_token')
    fb_api_url = config.get(config_section, 'fb_api_url')
    secret = config.get(config_section, 'secret')
    verify_token = config.get(config_section, 'verify_token')
    post_message_url = fb_api_url + fb_page_token

# set up server and aiml engine
app = Flask(__name__)
k = aiml.Kernel()
k.learn('std-startup.xml')
k.respond('load aiml b')
if config.has_section('botprofile'):
    for key, val in config.items('botprofile'):
        k.setBotPredicate(key, val)


@app.route('/')
def index():
    return('Hello world')


@app.route('/' + secret, methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        if verify_token == request.args.get('hub.verify_token'):
            return request.args.get('hub.challenge')
        else:
            return 'invalid token', 400

    elif request.method == 'POST':
        data = request.get_json()
        for entry in data['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    data = json.dumps({
                        'recipient': {'id': message['sender']['id']},
                        'message': {'text': k.respond(message['message']['text'])}
                    })
                    res = requests.post(post_message_url, headers={'Content-Type': 'application/json'}, data=data)
                    pprint(res.text)
        return data, 200

    return 'invalid request', 400

if __name__ == '__main__':
    app.run()
