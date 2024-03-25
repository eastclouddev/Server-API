from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_reviews_01(client_fixture: TestClient):
    
    response = client_fixture.patch(
        "/reviews/responses/1",
        json={
            "content": "更新済み",
            "is_read": True
        }  
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "review_request_id" in response.json()
    assert "user_id" in response.json()
    assert "parent_response_id" in response.json()
    assert "content" in response.json()
    assert "is_read" in response.json()
    assert "updated_at" in response.json()



"""取得失敗パターン"""
def test_reviews_02(client_fixture: TestClient):

    response = client_fixture.patch(
       "/reviews/responses/999",
        json={
            "content": "更新済み",
            "is_read": True
        }  
    )

    assert response.status_code == 404



