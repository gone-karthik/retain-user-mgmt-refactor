import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_user_success(client):
    resp = client.get("/user/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "id" in data and data["id"] == 1

def test_get_user_not_found(client):
    resp = client.get("/user/99999")  # Assuming DB has <99 users
    assert resp.status_code == 404
