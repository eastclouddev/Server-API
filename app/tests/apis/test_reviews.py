from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_reviews_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/mentors/2/students/reviews"
    )
    
    assert response.status_code == 200
    assert "id" in response.json()["reviews"][0]
    assert "title" in response.json()["reviews"][0]
    assert "content" in response.json()["reviews"][0]
    assert "curriculum_id" in response.json()["reviews"][0]
    assert "created_at" in response.json()["reviews"][0]
    assert "is_read" in response.json()["reviews"][0]
    assert "is_closed" in response.json()["reviews"][0]






