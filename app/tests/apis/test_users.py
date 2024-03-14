from fastapi.testclient import TestClient


def test_update_password_01(client_fixture: TestClient):
    """メールアドレスを変更せずに更新"""
    response = client_fixture.patch(
        "/users/1",
        json={
            "first_name": "華子",
            "last_name": "田中",
            "first_name_kana": "ハナコ",
            "last_name_kana": "タナカ",
            "email": "hanako@example.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == None


def test_update_password_02(client_fixture: TestClient):
    """他のユーザーに登録されているメールアドレスに変更し更新"""
    response = client_fixture.patch(
        "/users/2",
        json={
            "first_name": "太郎!",
            "last_name": "小林!",
            "first_name_kana": "タロウ",
            "last_name_kana": "コバヤシ",
            "email": "hanako@example.com"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is already in use."}


def test_update_password_03(client_fixture: TestClient):
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


