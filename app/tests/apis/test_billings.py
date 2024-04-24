from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

"""請求履歴詳細取得"""
def test_find_billing_details_01(client_fixture: TestClient):
    """paidではない場合"""
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

def test_find_billing_details_02(client_fixture: TestClient):
    """paidの場合"""
    response = client_fixture.get(
        "/billings/3"
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

def test_find_billing_details_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get(
        "/billings/10"
    )

    assert response.status_code == 404