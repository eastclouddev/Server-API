from datetime import datetime

from fastapi.testclient import TestClient



def test_find_receipt_01(client_fixture: TestClient):
    """"""
    response = client_fixture.get(
        "/receipts/1"
    )
    assert response.status_code == 200
    assert response.json()["receipt_id"] == 1
    assert response.json()["company_id"] == 1
    assert response.json()["billing_id"] == 1
    assert response.json()["date"] == datetime.now().strftime("%Y-%m-%d")
    assert response.json()["amount"] == 10000.00
    assert response.json()["received_from"] == "A社"
    assert response.json()["payment_method"] == "クレジットカード"

def test_find_receipt_02(client_fixture: TestClient):
    """"""
    response = client_fixture.get(
        "/receipts/100"
    )
    assert response.status_code == 404
