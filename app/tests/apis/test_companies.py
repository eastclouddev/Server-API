from fastapi.testclient import TestClient


def test_create_companies_01(client_fixture: TestClient):
    """会社情報の作成"""
    response = client_fixture.post(
        "/companies",
        json={
            "name": "A社",
            "prefecture": "A都",
            "city": "A区",
            "town": "A町",
            "address": "建物A",
            "postal_code": "000-0000",
            "phone_number": "000-0000-0000",
            "email": "aaa@mail.com"
        }
    )
    assert response.status_code == 200
    assert response.json()["company_id"] == 1
    assert response.json()["name"] == "A社"
    assert response.json()["prefecture"] == "A都"
    assert response.json()["city"] == "A区"
    assert response.json()["town"] == "A町"
    assert response.json()["address"] == "建物A"
    assert response.json()["postal_code"] == "000-0000"
    assert response.json()["phone_number"] == "000-0000-0000"
    assert response.json()["email"] == "aaa@mail.com"
    assert "company_id" in response.json()
    assert "name" in response.json()
    assert "prefecture" in response.json()
    assert "city" in response.json()
    assert "town" in response.json()
    assert "address" in response.json()
    assert "postal_code" in response.json()
    assert "phone_number" in response.json()
    assert "email" in response.json()

def test_create_companies_02(client_fixture: TestClient):
    """スキーマでのエラー"""
    response = client_fixture.post(
        "/companies",
        json={
            "name": 123,
            "prefecture": "A都",
            "city": "A区",
            "town": "A町",
            "address": "建物A",
            "postal_code": "000-0000",
            "phone_number": "000-0000-0000",
            "email": "aaa@mail.com"
        }
    )
    assert response.status_code == 422
