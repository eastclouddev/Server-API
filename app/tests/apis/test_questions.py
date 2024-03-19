from fastapi.testclient import TestClient


def test_create_answers_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/questions/1/answers",
        json={
            "user_id": "1",
            "content": "質問への回答です"
        }
    )

    assert response.status_code == 201
    assert "answer_id" in response.json()
    assert "question_id" in response.json()
    assert "user_id" in response.json()
    assert "content" in response.json()

# Abnormal 01: question not-found
def test_create_answers_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/questions/100/answers",
        json={
            "user_id": "1",
            "content": "質問への回答です"
        }
    )

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Question not found."
