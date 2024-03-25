from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_login_01(client_fixture: TestClient):
    """受け取ったpasswordとemailが元の情報と一致"""
    response = client_fixture.post(
        "/login",
        json={
            "email": "aaa@gmail.com",
            "password": "test1234",
            "device_info": {
                "device_type": "smartphone",
                "device_name": "iPhone12"
            }
        }   
    )


    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "access_token" in response.json()
    assert "expires_in" in response.json()
    assert "role" in response.json()


"""取得失敗パターン"""
def test_login_02(client_fixture: TestClient):
    """受け取ったemailとpasswordが元の情報と不一致"""
    response = client_fixture.post(
        "/login",
        json={
            "email": "bbb@gmail.com",
            "password": "zzzpassword",
            "device_info": {
                "device_type": "smartphone",
                "device_name": "iPhone11"
            }
        }   
    )


    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid email or password."}

