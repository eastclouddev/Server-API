from fastapi.testclient import TestClient

"""カリキュラムのレビュー一覧"""

"""カリキュラム詳細取得"""

"""質問投稿作成"""


"""レビュー投稿作成"""
def test_create_review_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/curriculums/1/reviews",
        json={
                "user_id": 1,
                "title": "string",
            "content": "string",
            "is_closed": False
        }
    )

    assert response.status_code == 201
    assert "user_id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "is_closed" in response.json()

def test_create_review_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.post(
        "/curriculums/123/reviews",
        json={
            "user_id": 1,
            "title": "string",
            "content": "string",
            "is_closed": False
            } 
    )

    assert response.status_code == 404 

"""テスト詳細取得"""
def test_find_test_details_01(client_fixture: TestClient):
    response = client_fixture.get(
        "curriculums/1/test"
    )
    assert response.status_code == 200
    assert "curriculum_id" in response.json()
    assert "tests" in response.json()
    assert "test_id" in response.json()["tests"][0]
    assert "question" in response.json()["tests"][0]
    assert "options" in response.json()["tests"][0]
    assert "correct_answer" in response.json()["tests"][0]
    assert "explanation" in response.json()["tests"][0]
    assert "media_content_url" in response.json()["tests"][0]

def test_find_test_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get(
        "curriculums/100/test"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Test content not found for the specified curriculum."

"""カリキュラムの質問一覧"""
def test_find_question_list_in_curriculum_01(client_fixture: TestClient):

    response = client_fixture.get("/curriculums/1/questions")
    
    assert response.status_code == 200
    assert "question_id" in response.json()["questions"][0]
    assert "curriculum_id" in response.json()["questions"][0]
    assert "user_id" in response.json()["questions"][0]
    assert "title" in response.json()["questions"][0]
    assert "content" in response.json()["questions"][0]
    assert "media_content" in response.json()["questions"][0]
    assert "url" in response.json()["questions"][0]["media_content"][0]

def test_find_question_list_in_curriculum_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/curriculums/123/questions")

    assert response.status_code == 404
    assert response.json()["detail"] == "Questions not found for the specified curriculum."

