import os
import pytest
from flask import jsonify
import boto3
from moto import mock_aws

os.environ['AWS_REGION'] = 'eu-west-2'
os.environ['AWS_Q1'] = 'testing'
os.environ['AWS_Q2'] = 'testing'
os.environ['AWS_Q3'] = 'testing'
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'

from app import create_app


@pytest.fixture(scope='function')
def app():
    
    with mock_aws():
        sqs = boto3.client('sqs', region_name='eu-west-2')
    
        app = create_app()
        app.config.update({
            "TESTING": True,
        })

        queue_name = "testing"
        queue_url = sqs.create_queue(
            QueueName='testing'
        )['QueueUrl']

        yield app


@pytest.fixture()
def client(app):
    with app.app_context():
        return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_get_health(client):
    response = client.get("/health")
    assert b'{"status":"Healthy"}\n' in response.data

def test_get_index(client):
    response = client.get("/")
    assert response.status_code == 200

def test_post_invalid_message(client):
    data = { "desc": "desc", "prio": 0}
    response = client.post("/", json=data)
    assert response.data == b'Invalid message'

def test_post_invalid_prio(client):
    data = {"title": "test", "desc": "desc", "prio": -1}
    response = client.post("/", json=data)
    assert response.data == b'Invalid priority'

@mock_aws
def test_post_valid(client):
    with mock_aws():
        data = {"title": "pytest", "desc": "pytest desc", "prio": 0}
        response = client.post("/", json=data)
        assert response.status_code == 200