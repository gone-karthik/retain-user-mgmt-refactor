from app import app
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_login_success(client):
    resp = client.post("/login", json={"username": "admin", "password": "secret"})
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "success"

@pytest.mark.parametrize("u,p", [("fake", "fake"), ("admin", "wrong")])
def test_login_fail(client, u, p):
    resp = client.post("/login", json={"username": u, "password": p})
    assert resp.status_code == 401
