from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_questions_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/questions/1"
    )

    assert response.status_code == 200
    assert "id" in response.json()["question"]
    assert "curriculum_id" in response.json()["question"]
    assert "user_id" in response.json()["question"]
    assert "title" in response.json()["question"]
    assert "content" in response.json()["question"]
    assert "media_content" in response.json()["question"]
    assert "is_closed" in response.json()["question"]
    assert "created_at" in response.json()["question"]

    assert "id" in response.json()["answer"][0]
    assert "question_id" in response.json()["answer"][0]
    assert "user_id" in response.json()["answer"][0]
    assert "parent_answer_id" in response.json()["answer"][0]
    assert "content" in response.json()["answer"][0]
    assert "media_content" in response.json()["answer"][0]
    assert "is_read" in response.json()["answer"][0]
    assert "created_at" in response.json()["answer"][0]
    


"""取得失敗パターン"""
def test_questions_02(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/questions/9999"
    )

    assert response.status_code == 404