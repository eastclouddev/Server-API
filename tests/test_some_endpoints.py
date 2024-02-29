# app/tests/test_some_endpoint.py
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user():
    data = {"email": "test@example.com", "username": "testuser", "password": "password"}
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["username"] == data["username"]
    assert "id" in response.json()

def test_read_user():
    data = {"email": "test@example.com", "username": "testuser", "password": "password"}
    response = client.post("/users/", json=data)
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["username"] == data["username"]
    assert response.json()["id"] == user_id

def test_update_user():
    data = {"email": "test@example.com", "username": "testuser", "password": "password"}
    response = client.post("/users/", json=data)
    user_id = response.json()["id"]
    data["username"] = "newusername"
    response = client.put(f"/users/{user_id}", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["username"] == data["username"]
    assert response.json()["id"] == user_id

def test_delete_user():
    data = {"email": "test@example.com", "username": "testuser", "password": "password"}
    response = client.post("/users/", json=data)
    user_id = response.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"id": user_id} 

