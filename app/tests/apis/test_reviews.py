from fastapi.testclient import TestClient

# ファイルが違う
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


"""レビュー回答更新"""
def test_update_review_response_01(client_fixture: TestClient):
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

def test_update_review_response_ABNORMAL_02(client_fixture: TestClient):
    response = client_fixture.patch(
        "/reviews/responses/999",
        json={
            "content": "更新済み",
            "is_read": True
        }  
    )

    assert response.status_code == 404

"""レビュー更新（受講生）"""
def test_update_review_request_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/reviews/1",
        json={
            "title":"title",
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

def test_update_review_request_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/reviews/999",
        json={
            "title": "title",
            "content": "更新済み",
            "is_closed": True
        }  
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Curriculum not found."

"""レビュースレッド詳細"""
def test_find_review_thread_details_01(client_fixture: TestClient):

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

def test_find_review_thread_details_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/reviews/123/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review request not found."