from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_billings_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/billings/1"
    )

    assert response.status_code == 200
    assert "billing_id" in response.json()
    assert "company_id" in response.json()
    assert "date" in response.json()
    assert "amount" in response.json()
    assert "status" in response.json()
    assert "payment_details" in response.json()
    assert "payment_method" in response.json()["payment_details"]
    assert "payment_date" in response.json()["payment_details"]

"""取得失敗パターン"""
def test_billings_02(client_fixture: TestClient):

    response = client_fixture.get(
        "/billings/10"
    )

    assert response.status_code == 404
