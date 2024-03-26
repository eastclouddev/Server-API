from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_reviews_01(client_fixture: TestClient):
    
    response = client_fixture.patch(
        "/reviews/1",
        json={
            "title":"title OK",
            "content": "更新済み",
            "is_closed": True
        }  
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "is_closed" in response.json()
    assert "updated_at" in response.json()




"""取得失敗パターン"""
def test_reviews_02(client_fixture: TestClient):

    response = client_fixture.patch(
       "/reviews/999",
        json={
            "title": "title1",
            "content": "更新済み",
            "is_closed": True
        }  
    )

    assert response.status_code == 404