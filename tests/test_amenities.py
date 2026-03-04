import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_create_amenity_success(client):
    data = {"name": "Wi-Fi"}
    resp = client.post("/api/v1/amenities/", json=data)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["name"] == "Wi-Fi"


def test_create_amenity_invalid(client):
    data = {"name": ""}
    resp = client.post("/api/v1/amenities/", json=data)
    assert resp.status_code == 400


def test_get_amenity_by_id(client):
    data = {"name": "Pool"}
    resp = client.post("/api/v1/amenities/", json=data)
    amenity_id = resp.get_json()["id"]

    resp = client.get(f"/api/v1/amenities/{amenity_id}")
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Pool"


def test_list_amenities(client):
    resp = client.get("/api/v1/amenities/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
