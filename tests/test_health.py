import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_health_endpoint(client):
    resp = client.get("/")
    assert resp.status_code == 200
