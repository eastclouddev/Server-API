from fastapi.testclient import TestClient

"""成功パターン"""
def test_users_01(client_fixture: TestClient):
    
    
    # ペイロード作成
    from datetime import datetime, timedelta
    import jwt
    access_payload = {
        'email': 'update@gmail.com'
    }

    #  トークン作成  
    token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')



    response = client_fixture.get(
        f"/users/1/email/confirm_change?token={token}",
    
    )

    assert response.status_code == 200
    assert "message" in response.json()


"""失敗パターン"""
def test_users_02(client_fixture: TestClient):


    
    # ペイロード作成
    from datetime import datetime, timedelta
    import jwt
    access_payload = {
        'email': 'update@gmail.com'
    }

    #  トークン作成  
    token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')



    response = client_fixture.get(
       f"/users/999/email/confirm_change?token={token}",
        
    )

    assert response.status_code == 400

def test_users_manage_01(client_fixture: TestClient):

    response = client_fixture.get("/users/?role=student&page=1&limit=5")
    assert response.status_code == 200
    assert "user_id" in response.json()["users"][0]
    assert "first_name" in response.json()["users"][0]
    assert "last_name" in response.json()["users"][0]
    assert "email" in response.json()["users"][0]
    assert "role" in response.json()["users"][0]
    assert "last_login" in response.json()["users"][0]

def test_no_users_manage_01(client_fixture: TestClient):

    response = client_fixture.get("/users/?role=hoge&page=1&limit=5")
    assert response.status_code == 200
    assert response.json()["users"] == []
    





