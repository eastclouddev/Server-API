from fastapi.testclient import TestClient
from tests.conftest import session_fixture
import jwt

from models.devices import Devices
from models.access_token import AccessToken

"""成功パターン   ログアウト時にデバイス情報の削除(トークンに含まれるuser_idがデータベースに存在する"""
def  test_logout_01(client_fixture: TestClient,session_fixture):
     response = client_fixture.post(
          "/logout",
          headers = {"authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwidXNlcl9pZCI6MX0.NRWoe4jscAMyFRuYZ4zKcUdnfRCEP_s9nDpc0yM8DMM"}
     )
     assert response.status_code == 200
     assert response.json() ==  None
     
     device_info = session_fixture.query(Devices).filter(Devices.user_id == 1).first()
     assert device_info == None

"""成功パターン   ログアウト時にリフレッシュトークンの削除(トークンに含まれるuser_idがデータベースに存在する"""
def  test_logout_02(client_fixture: TestClient,session_fixture):
     response = client_fixture.post(
          "/logout",
          headers = {"authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwidXNlcl9pZCI6MX0.NRWoe4jscAMyFRuYZ4zKcUdnfRCEP_s9nDpc0yM8DMM"}
     )
     assert response.status_code == 200
     assert response.json() ==  None
     
     refresh_token = session_fixture.query(AccessToken).filter(AccessToken.user_id == 1).first()
     assert refresh_token == None

"""失敗パターン   (トークンに含まれるuser_idがデータベースに存在しない)"""
def test_find_by_id_ABNORMAL_01(client_fixture: TestClient):
     response = client_fixture.post(
         "/logout",
          headers = {"authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwidXNlcl9pZCI6MTAwfQ.OjkMBPPVkZiPGq0K8IeDSbp0GSmSwJY-hpBzmaeVjlo"}
     )
     assert response.status_code == 401
     assert response.json()["detail"] == "Logout failed."

