from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass


"""ニュース詳細取得"""

"""ニュース一覧取得"""

"""ニュース作成"""

"""ニュース更新"""
def test_update_news_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/news/1",
        json={
            "title": "string",
            "content": "string",
            "is_published": False,
            "published_at": "2024-03-01T10:00:00Z"
        }
    )

    assert response.status_code == 200
    assert "title" in  response.json()
    assert "content" in response.json()
    assert "is_published" in response.json()
    assert "published_at" in response.json()

def test_update_news_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/news/123",
        json={
            "title": "string",
            "content": "string",
            "is_published": False,
            "published_at": "2024-03-01T10:00:00Z"
        }
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "News not found."
