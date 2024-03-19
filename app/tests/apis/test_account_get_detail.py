from fastapi.testclient import TestClient

def test_find_all_01(client_fixture: TestClient):
    response = client_fixture.get("/users/1")
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "first_name_kana" in response.json()
    assert "last_name_kana" in response.json()
    assert "email" in response.json()
    assert "role" in response.json()
    assert "last_login" in response.json()

def test_find_by_id_ABNORMAL_01(client_fixture: TestClient):
     response = client_fixture.get("/users/500")
     assert response.status_code == 404
     assert response.json()["detail"] == "User not found."
