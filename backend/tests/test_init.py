import requests
from fastapi.testclient import TestClient

from app import settings
from app.main import app

client = TestClient(app)


def test_elasticsearch():
    es_url = settings.ES_URL
    r = requests.get(es_url)
    assert r.ok, r.text


def test_root():
    r = client.get("/")
    assert r.ok


def test_ping():
    r = client.get("/ping")
    assert r.json() is True


def test_ping_dependencies():
    r = client.get("/ping", params={"dependencies": True})
    assert r.json() is True


def test_es_status():
    r = client.get("/es-status")
    res = r.json()
    assert res is not None
    assert isinstance(res, dict)
