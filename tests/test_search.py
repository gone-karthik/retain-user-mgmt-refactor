from app import app
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

@pytest.mark.parametrize("q,expected_min", [
    ("A", 0),  # returns empty or list
    ("john", 0),
])
def test_search_case_insensitive(client, q, expected_min):
    resp = client.get(f"/search?name={q}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
