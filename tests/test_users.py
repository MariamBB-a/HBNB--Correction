import pytest
from app import create_app
import json


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_create_user_success(client):
    data = {"first_name": "John", "last_name": "Doe",
            "email": "john@example.com", "password": "1234"}
    resp = client.post("/api/v1/users/", json=data)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["first_name"] == "John"
    assert "id" in body


def test_create_user_duplicate_email(client):
    data = {"first_name": "Jane", "last_name": "Doe",
            "email": "john@example.com", "password": "1234"}
    resp = client.post("/api/v1/users/", json=data)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_get_user_by_id(client):
    # Create user first
    data = {"first_name": "Alice", "last_name": "Smith",
            "email": "alice@example.com", "password": "pass"}
    resp = client.post("/api/v1/users/", json=data)
    user_id = resp.get_json()["id"]

    resp = client.get(f"/api/v1/users/{user_id}")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["email"] == "alice@example.com"


def test_get_invalid_user(client):
    resp = client.get("/api/v1/users/invalid-id")
    assert resp.status_code == 404


def test_list_users(client):
    resp = client.get("/api/v1/users/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)


def test_update_user_success(client):
    data = {"first_name": "Bob", "last_name": "Marley",
            "email": "bob@example.com", "password": "abcd"}
    resp = client.post("/api/v1/users/", json=data)
    user_id = resp.get_json()["id"]

    update_data = {"first_name": "Bobby",
                   "last_name": "Marley", "email": "bob@example.com"}
    resp = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["first_name"] == "Bobby"


def test_update_user_invalid_id(client):
    update_data = {"first_name": "Bobby",
                   "last_name": "Marley", "email": "bob@example.com"}
    resp = client.put("/api/v1/users/invalid-id", json=update_data)
    assert resp.status_code == 404
