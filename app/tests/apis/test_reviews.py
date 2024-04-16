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

def test_review_thread_01(client_fixture: TestClient):

    response = client_fixture.get("/reviews/1/")

    assert response.status_code == 200
    assert "id" in response.json()["review_request"]
    assert "curriculum_id" in response.json()["review_request"]
    assert "user_id" in response.json()["review_request"]
    assert "title" in response.json()["review_request"]
    assert "content" in response.json()["review_request"]
    assert "is_closed" in response.json()["review_request"]
    assert "created_at" in response.json()["review_request"]
    assert "updated_at" in response.json()["review_request"]
    assert "id" in response.json()["responses"][0]
    assert "review_request_id" in response.json()["responses"][0]
    assert "user_id" in response.json()["responses"][0]
    assert "parent_response_id" in response.json()["responses"][0]
    assert "content" in response.json()["responses"][0]
    assert "is_read" in response.json()["responses"][0]
    assert "created_at" in response.json()["responses"][0]

def test_review_thread_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/reviews/123/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review request not found."