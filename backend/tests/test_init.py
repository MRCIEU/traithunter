from starlette.testclient import TestClient

from app.main import app

def test_ping():
    with TestClient(app) as client:
        r = client.get("/ping")
    assert r.ok
