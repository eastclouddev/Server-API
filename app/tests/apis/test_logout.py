from fastapi.testclient import TestClient


async def test_logout_01(client_fixture: TestClient):
     response = client_fixture.post(
          "/logout",
          headers = {"authorization":"hello"}
)
     assert response.status_code == 200
     assert response.json() ==  {}
     
async def test_find_by_id_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post("/logout")
    assert response.status_code == 401
    assert response.json()["detail"] == "You are not authorized to perform this action."
