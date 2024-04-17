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