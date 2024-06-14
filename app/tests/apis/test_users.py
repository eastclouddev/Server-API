from datetime import datetime, timedelta
import jwt

from fastapi.testclient import TestClient


"""アカウント更新"""
def test_update_user_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/users/1",
        json={
            "first_name": "華子",
            "last_name": "田中",
            "first_name_kana": "ハナコ",
            "last_name_kana": "タナカ",
            "email": "aaa@mail.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == None

def test_update_user_02(client_fixture: TestClient):
    response = client_fixture.patch(
        "/users/1",
        json={
            "first_name": "華子",
            "last_name": "田中",
            "first_name_kana": "ハナコ",
            "last_name_kana": "タナカ",
            "email": "abcdefg@mail.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == None


def test_update_user_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/users/2",
        json={
            "first_name": "太郎!",
            "last_name": "小林!",
            "first_name_kana": "タロウ",
            "last_name_kana": "コバヤシ",
            "email": "aaa@mail.com"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is already in use."}


def test_update_user_ABNORMAL_02(client_fixture: TestClient):
    response = client_fixture.patch(
        "/users/123",
        json={
            "first_name": "華子",
            "last_name": "田中",
            "first_name_kana": "ハナコ",
            "last_name_kana": "タナカ",
            "email": "hanako123@example.com"
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication failed."}

"""アカウント詳細取得"""
def test_find_user_details_01(client_fixture: TestClient):
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

def test_find_user_details_ABNORMAL_01(client_fixture: TestClient):
     response = client_fixture.get("/users/500")
     assert response.status_code == 404
     assert response.json()["detail"] == "User not found."

# """メールアドレス認証と更新"""
# def test_email_confirm_change_01(client_fixture: TestClient):
    
#     # ペイロード作成
#     access_payload = {
#         'email': 'update@gmail.com'
#     }

#     # トークン作成  
#     token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')

#     response = client_fixture.get(
#         f"/users/1/email/confirm_change?token={token}",
#     )

#     assert response.status_code == 200
#     assert "message" in response.json()


# def test_email_confirm_change_ABNORMAL_01(client_fixture: TestClient):

#     # ペイロード作成
#     access_payload = {
#         'email': 'update@gmail.com'
#     }

#     # トークン作成  
#     token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')

#     response = client_fixture.get(
#        f"/users/999/email/confirm_change?token={token}",
#     )

#     assert response.status_code == 400

"""受講生一覧(管理者)"""
def test_find_student_list_01(client_fixture: TestClient):

    response = client_fixture.get("/users?role=student&page=1&limit=5")
    assert response.status_code == 200
    assert "user_id" in response.json()["users"][0]
    assert "name" in response.json()["users"][0]
    assert "company_name" in response.json()["users"][0]
    assert "email" in response.json()["users"][0]
    assert "role" in response.json()["users"][0]
    assert "is_enable" in response.json()["users"][0]
    assert "last_login" in response.json()["users"][0]

def test_find_student_list_02(client_fixture: TestClient):

    response = client_fixture.get("/users?role=hoge&page=1&limit=5")
    assert response.status_code == 200
    assert response.json()["users"] == []
    
"""有効アカウント数取得"""
def test_find_number_of_accounts_01(client_fixture: TestClient):
    response = client_fixture.get("/users/counts/")

    assert response.status_code == 200
    assert "role_counts" in response.json()



