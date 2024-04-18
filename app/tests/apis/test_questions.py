from fastapi.testclient import TestClient

"""質問投稿作成"""
"""成功パターン"""
def test_questions_01(client_fixture: TestClient):
    response = client_fixture.post(
       "/curriculums/1/questions",
       json={
            "user_id": 1,
            "title": "string",
            "content": "string",
            "media_content": {
                "url": "string"
            }
        }  
    )

    assert response.status_code == 201
    assert "user_id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "media_content" in response.json()
    assert "url" in response.json()["media_content"][0]


"""失敗パターン"""
def test_questions_02(client_fixture: TestClient):

    response = client_fixture.post(
       "/curriculums/123/questions",
        json={
            "user_id": 1,
            "title": "string",
            "content": "string",
            "media_content": {
                "url": "string"
            }
        } 
    )

    assert response.status_code == 404


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

def test_update_question_02(client_fixture: TestClient):
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
