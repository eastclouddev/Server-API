from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass



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