from fastapi.testclient import TestClient

"""質問回答投稿作成"""
def test_create_answers_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/questions/1/answers",
        json={
            "user_id": "1",
            "parent_answer_id": 1,
            "content": "質問への回答です",
            "media_content": [
                {"url": "aaa.com"},
                {"url": "bbb.com"}
            ]
        }
    )

    assert response.status_code == 201
    assert "answer_id" in response.json()
    assert "question_id" in response.json()
    assert "parent_answer_id" in response.json()
    assert "user" in response.json()
    assert "media_content" in response.json()
    assert "content" in response.json()
    assert "created_at" in response.json()

def test_create_answers_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/questions/999/answers",
        json={
            "user_id": "1",
            "parent_answer_id": 1,
            "content": "質問への回答です",
            "media_content": [
                {"url": "aaa.com"},
                {"url": "bbb.com"}
            ]
        }
    )

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Question not found."

"""質問スレッド詳細取得"""
def test_find_question_thread_details_01(client_fixture: TestClient):
    response = client_fixture.get("/questions/1")

    assert response.status_code == 200
    assert "id" in response.json()["question"]
    assert "curriculum_id" in response.json()["question"]
    assert "user" in response.json()["question"]
    assert "title" in response.json()["question"]
    assert "objective" in response.json()["question"]
    assert "current_situation" in response.json()["question"]
    assert "research" in response.json()["question"]
    assert "content" in response.json()["question"]
    assert "media_content" in response.json()["question"]
    assert "is_closed" in response.json()["question"]
    assert "created_at" in response.json()["question"]
    assert "id" in response.json()["answer"][0]
    assert "question_id" in response.json()["answer"][0]
    assert "user" in response.json()["answer"][0]
    assert "parent_answer_id" in response.json()["answer"][0]
    assert "content" in response.json()["answer"][0]
    assert "media_content" in response.json()["answer"][0]
    assert "created_at" in response.json()["answer"][0]

def test_find_question_thread_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/questions/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found."

"""質問回答更新（受講生、メンター）"""
def test_update_answer_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "questions/answers/1",
        json={
            "content": "更新後の内容",
            "media_content": {
                "url": "sample.com"
            },
            "is_read": True
        }
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "question_id" in response.json()
    assert "user_id" in response.json()
    assert "parent_answer_id" in response.json()
    assert "content" in response.json()
    assert response.json()["content"] == "更新後の内容"
    assert "media_content" in response.json()
    assert response.json()["media_content"] == {"url": "sample.com"}
    assert "is_read" in response.json()
    assert response.json()["is_read"] == True
    assert "updated_at" in response.json()

def test_update_answer_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "questions/answers/100",
        json={
            "content": "更新後の内容",
            "media_content": {
                "url": "sample.com"
            },
            "is_read": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Answer not found."

"""質問編集"""
def test_update_question_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "questions/1",
        json={
            "title": "更新後のタイトル",
            "content": "更新後の内容",
            "media_content": {
                "url": "sample.com"
            },
            "is_closed": True
        }
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "curriculum_id" in response.json()
    assert "user_id" in response.json()  
    assert "title" in response.json()
    assert response.json()["title"] == "更新後のタイトル"
    assert "content" in response.json()
    assert response.json()["content"] == "更新後の内容"
    assert "media_content" in response.json()
    assert response.json()["media_content"] == {"url": "sample.com"}
    assert "is_closed" in response.json()
    assert response.json()["is_closed"] == True
    assert "updated_at" in response.json()

def test_update_question_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "questions/999",
        json={
            "title": "更新後のタイトル",
            "content": "更新後の内容",
            "media_content": {
                "url": "sample.com"
            },
            "is_closed": True
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found."
