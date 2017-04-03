import os
import pytest
import server
import aiml
import json
import requests
import responses


@pytest.fixture
def client(request):
    return server.app.test_client()


def test_index(client):
    rv = client.get('/')
    assert b'Hello world' in rv.data


def test_verify_token(client):
    challenge = 'challenge'
    rv = client.get('/' + server.secret + '?hub.verify_token=' + server.verify_token + '&hub.challenge=' + challenge)
    assert challenge == rv.data


def test_invalid_token(client):
    wrong_token = 'wrong_token'
    rv = client.get('/' + server.secret + '?hub.verify_token=' + wrong_token + '&hub.challenge=challenge')
    assert 'invalid token' == rv.data


@responses.activate
def test_respond_message(client):
    sender_id = '1350988261628992'
    post_data = {
        'entry': [
            {
                'messaging': [
                    {
                        'message': {
                            'mid': 'mid.$cAADiAXW_j1JhY7q9DlbMnV0WsISf',
                            'seq': 49,
                            'text': 'hi'
                        },
                        'recipient': {'id': '203364796819901'},
                        'sender': {'id': sender_id},
                        'timestamp': 1491200210190L
                    }
                ]
            }
        ]
    }

    server.post_message_url = 'http://post_message_url'
    responses.add(
        responses.POST,
        server.post_message_url,
        body=json.dumps({'recipient_id': sender_id, 'message_id': 'mid.$cAADiAXW_j1JhY7rA81bMnV4WH3PS'}),
        status=200,
        content_type='application/json'
    )

    rv = client.post('/' + server.secret, headers={'Content-Type': 'application/json'}, data=json.dumps(post_data))
    assert len(responses.calls) == 1
    assert rv.status_code == 200
    assert rv.data == json.dumps({'message': {'text': 'What can I call you?'}, 'recipient': {'id': sender_id}})
