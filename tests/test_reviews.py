import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def create_user(client, email="user@example.com"):
    data = {"first_name": "User", "last_name": "Test",
            "email": email, "password": "1234"}
    return client.post("/api/v1/users/", json=data).get_json()["id"]


def create_place(client, owner_id):
    data = {"title": "Villa", "owner": owner_id}
    return client.post("/api/v1/places/", json=data).get_json()["id"]


def test_create_review_success(client):
    user_id = create_user(client)
    place_id = create_place(client, user_id)
    data = {"user_id": user_id, "place_id": place_id,
            "comment": "Great!", "rating": 5}
    resp = client.post("/api/v1/reviews/", json=data)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["rating"] == 5


def test_create_review_invalid_rating(client):
    user_id = create_user(client, "u2@example.com")
    place_id = create_place(client, user_id)
    data = {"user_id": user_id, "place_id": place_id,
            "comment": "Bad", "rating": 6}
    resp = client.post("/api/v1/reviews/", json=data)
    assert resp.status_code == 400


def test_get_review_by_id(client):
    user_id = create_user(client, "u3@example.com")
    place_id = create_place(client, user_id)
    data = {"user_id": user_id, "place_id": place_id,
            "comment": "Nice", "rating": 4}
    resp = client.post("/api/v1/reviews/", json=data)
    review_id = resp.get_json()["id"]

    resp = client.get(f"/api/v1/reviews/{review_id}")
    assert resp.status_code == 200


def test_delete_review(client):
    user_id = create_user(client, "u4@example.com")
    place_id = create_place(client, user_id)
    data = {"user_id": user_id, "place_id": place_id,
            "comment": "Delete me", "rating": 3}
    resp = client.post("/api/v1/reviews/", json=data)
    review_id = resp.get_json()["id"]

    resp = client.delete(f"/api/v1/reviews/{review_id}")
    assert resp.status_code == 200
    resp = client.get(f"/api/v1/reviews/{review_id}")
    assert resp.status_code == 404
