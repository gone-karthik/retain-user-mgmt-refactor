import pytest
from app import app

@pytest.fixture
def client():
    """
    Standard pytest fixture to create Flask test client.
    Using pytest’s auto fixture collection and Flask’s test_client().
    """
    app.config["TESTING"] = True
    return app.test_client()

def test_get_user_success(client):
    # Existing users seeded by init_db.py
    resp = client.get("/user/1")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, dict)
    assert body.get("id") == 1
    assert "name" in body and "email" in body

def test_get_user_not_found(client):
    # An ID that should not exist
    resp = client.get("/user/99999")
    assert resp.status_code == 404
