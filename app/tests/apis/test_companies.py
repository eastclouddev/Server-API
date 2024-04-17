from fastapi.testclient import TestClient



"""取得成功パターン"""
def test_get_users_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies/1/users/?role=admin&page=1&limit=2",
    )

    data = response.json()
    assert response.status_code == 200
    assert "users" in response.json()
    assert data["users"] 
    
    assert "user_id" in data["users"][0]
    assert "first_name" in data["users"][0]
    assert "last_name" in data["users"][0]
    assert "email" in data["users"][0]
    assert "role" in data["users"][0]
    assert "last_login" in data["users"][0]

"""取得失敗パターン"""
def test_get_users_02(client_fixture: TestClient):

    response = client_fixture.get(
       "/companies/999/users/?role=admin&page=1&limit=2",
    )

    assert response.status_code == 404


