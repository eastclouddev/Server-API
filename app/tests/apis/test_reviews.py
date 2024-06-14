from fastapi.testclient import TestClient


"""レビュー回答投稿"""
def test_create_review_resposne_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/reviews/1/responses",
        json={
            "user_id": 1,
            "parent_response_id": 1,
            "content": "回答",
            "media_content": [
                {"url": "aaa.com"},
                {"url": "bbb.com"}
            ]
        }  
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert "review_request_id" in response.json()
    assert "user" in response.json()
    assert "parent_response_id" in response.json()
    assert "content" in response.json()
    assert "media_content" in response.json()
    assert "created_at" in response.json()

def test_create_review_resposne_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/reviews/123/responses",
        json={
            "user_id": 1,
            "parent_response_id": 1,
            "content": "回答",
            "media_content": [
                {"url": "aaa.com"},
                {"url": "bbb.com"}
            ]
        }  
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Review request not found."

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
    assert "review_request" in response.json()
    assert "id" in response.json()["review_request"]
    assert "curriculum_id" in response.json()["review_request"]
    assert "user" in response.json()["review_request"]
    assert "title" in response.json()["review_request"]
    assert "content" in response.json()["review_request"]
    assert "media_content" in response.json()["review_request"]
    assert "created_at" in response.json()["review_request"]
    assert "review_responses" in response.json()
    assert "id" in response.json()["review_responses"][0]
    assert "review_request_id" in response.json()["review_responses"][0]
    assert "user" in response.json()["review_responses"][0]
    assert "parent_response_id" in response.json()["review_responses"][0]
    assert "content" in response.json()["review_responses"][0]
    assert "media_content" in response.json()["review_responses"][0]
    assert "created_at" in response.json()["review_responses"][0]

def test_find_review_thread_details_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/reviews/123/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review request not found."