from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

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