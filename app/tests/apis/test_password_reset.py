from datetime import datetime, timedelta
import jwt

from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass



def test_password_reset_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/password_reset",
        json={
            "email": "aaa@mail.com"
        }
    )

    assert response.status_code == 200

def test_password_reset_ABNORMAR_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/password_reset",
        json={
            "email": "aaabbbccc@mail.com"
        }
    )

    assert response.status_code == 404

def test_password_setting_01(client_fixture: TestClient):
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.now() + timedelta(seconds=3600),
        'user_id': 1,
        "email": "aaa@mail.com"
    }
    access_token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')

    response = client_fixture.post(
        "/password_reset/confirm",
        json={
            "token": access_token,
            "new_password": "1234Test!"
        }
    )

    assert response.status_code == 200

def test_password_setting_ABNORMAL_01(client_fixture: TestClient):
    """
    パスワードのポリシーエラー
    """
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.now() + timedelta(seconds=3600),
        'user_id': 1,
        "email": "aaa@mail.com"
    }
    access_token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')

    response = client_fixture.post(
        "/password_reset/confirm",
        json={
            "token": access_token,
            "new_password": "1234567890"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token or password does not meet the security requirements."

def test_password_setting_ABNORMAL_02(client_fixture: TestClient):
    """
    トークンの期限切れエラー
    """
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.now() + timedelta(seconds=-3600),
        'user_id': 1,
        "email": "aaa@mail.com"
    }
    access_token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')

    response = client_fixture.post(
        "/password_reset/confirm",
        json={
            "token": access_token,
            "new_password": "1234Test!"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token or password does not meet the security requirements."

