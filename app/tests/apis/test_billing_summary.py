from fastapi.testclient import TestClient


"""先月の請求金額合計取得"""
def test_find_billing_summary_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/billing_summary/last_month"
    )

    assert response.status_code == 200
    assert "month" in response.json()
    assert "total_billed_amount" in response.json()