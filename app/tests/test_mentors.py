from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_mentors_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/mentors/1/accounts"
    )

    assert response.status_code == 200
    assert "mentor_id" in response.json()
    assert "account_name" in response.json()
    assert "bank_name" in response.json()
    assert "branch_name" in response.json()
    assert "account_number" in response.json()
    assert "account_type" in response.json()

"""取得失敗パターン"""
def test_mentors_02(client_fixture: TestClient):

    response = client_fixture.get(
       "/mentors/111/accounts"
    )

    assert response.status_code == 404


