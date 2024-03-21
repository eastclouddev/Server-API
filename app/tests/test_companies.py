from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_mentors_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies/1"
    )

    assert response.status_code == 200
    assert "company_id" in response.json()
    assert "name" in response.json()
    assert "prefecture" in response.json()
    assert "city" in response.json()
    assert "town" in response.json()
    assert "address" in response.json()
    assert "postal_code" in response.json()
    assert "phone_number" in response.json()
    assert "email" in response.json()
    assert "created_at" in response.json()
    assert "updated_at" in response.json()



"""取得失敗パターン"""
def test_mentors_02(client_fixture: TestClient):

    response = client_fixture.get(
       "/companies/999"
    )

    assert response.status_code == 404


