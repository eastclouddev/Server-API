from fastapi.testclient import TestClient
from tests.conftest import session_fixture

from models.devices import Devices
from models.users import Users


"""取得成功パターン"""
def test_login_01(client_fixture: TestClient):
    """受け取ったpasswordとemailが元の情報と一致"""
    response = client_fixture.post(
        "/login",
        json={
            "email": "aaa@mail.com",
            "password": "test1234",
            "device_info": {
                "device_type": "PC(Win)",
                "device_name": "花子のPC",
                "uuid": "test1"
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
                "device_name": "iPhone11",
                "uuid": "test2"
            }
        }   
    )


    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid email or password."}

"""新規デバイス情報作成パターン"""
def test_login_03(client_fixture: TestClient,session_fixture):
    """リクエストボディのデバイス情報を追加"""
    response = client_fixture.post(
        "/login",
        json={
            "email": "test@mail.com",
            "password": "test1234",
            "device_info": {
                "device_type": "ひとり",
                "device_name": "いちだい",
                "uuid": "test3"
            }
        }   
    )


    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "access_token" in response.json()
    assert "expires_in" in response.json()
    assert "role" in response.json()

   
    user = session_fixture.query(Users).filter(Users.email == "test@mail.com").first()

    device = session_fixture.query(Devices).filter(Devices.user_id == user.id).first()

    assert device.user_id == user.id
    assert device.device_type == "ひとり"
    assert device.device_name == "いちだい"
    assert device.uuid == "test3"