from fastapi.testclient import TestClient

"""レビュー投稿作成"""
"""成功パターン"""
def test_reviews_01(client_fixture: TestClient):

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

"""失敗パターン"""
def test_rus_02(client_fixture: TestClient):

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