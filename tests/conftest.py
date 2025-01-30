import pytest
from flask import jsonify

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

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
    assert b"Healthy" in response.data

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


def test_post_valid(client):
    data = {"title": "pytest", "desc": "pytest desc", "prio": 0}
    response = client.post("/", json=data)
    assert response.status_code == 200