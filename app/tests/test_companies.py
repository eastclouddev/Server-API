from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_companies_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies"
    )

    assert response.status_code == 200
    assert "company_id" in response.json()["companies"][0]
    assert "name" in response.json()["companies"][0]
    assert "prefecture" in response.json()["companies"][0]
    assert "city" in response.json()["companies"][0]
    assert "town" in response.json()["companies"][0]
    assert "address" in response.json()["companies"][0]
    assert "postal_code" in response.json()["companies"][0]
    assert "phone_number" in response.json()["companies"][0]
    assert "email" in response.json()["companies"][0]
    assert "created_at" in response.json()["companies"][0]


