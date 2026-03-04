import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def create_user(client, email="owner@example.com"):
    data = {"first_name": "Owner", "last_name": "User",
            "email": email, "password": "1234"}
    resp = client.post("/api/v1/users/", json=data)
    return resp.get_json()["id"]


def test_create_place_success(client):
    owner_id = create_user(client)
    data = {
        "title": "Beach House",
        "description": "Nice view",
        "price": 120.0,
        "latitude": 34.0,
        "longitude": -118.0,
        "owner": owner_id
    }
    resp = client.post("/api/v1/places/", json=data)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Beach House"


def test_create_place_invalid_price(client):
    owner_id = create_user(client)
    data = {"title": "House", "price": -5,
            "latitude": 0, "longitude": 0, "owner": owner_id}
    resp = client.post("/api/v1/places/", json=data)
    assert resp.status_code == 400


def test_get_place_by_id(client):
    owner_id = create_user(client)
    data = {"title": "Cottage", "owner": owner_id}
    resp = client.post("/api/v1/places/", json=data)
    place_id = resp.get_json()["id"]

    resp = client.get(f"/api/v1/places/{place_id}")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Cottage"


def test_get_invalid_place(client):
    resp = client.get("/api/v1/places/invalid-id")
    assert resp.status_code == 404


def test_list_places(client):
    resp = client.get("/api/v1/places/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
