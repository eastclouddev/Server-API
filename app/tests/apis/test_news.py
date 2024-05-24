from datetime import datetime

from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass


"""ニュース詳細取得"""
def test_find_news_details_01(client_fixture: TestClient):
    response = client_fixture.get("/news/1")

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "published_at" in response.json()

def test_find_news_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/news/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "The requested news article was not found."

"""ニュース一覧取得"""
def test_find_news_list_01(client_fixture: TestClient):
    response = client_fixture.get("/news/?page=1&limit=2")
    assert response.status_code == 200
    assert "id" in response.json()["news"][0]
    assert "title" in response.json()["news"][0]
    assert "published_at" in response.json()["news"][0]
    assert "page" in response.json()
    assert "limit" in response.json()
    assert "total_pages" in response.json()
    assert "total_news" in response.json()

"""ニュース作成"""
def test_create_news_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/news",
        json={
            "title": "〇〇変更のお知らせ",
            "content": "Y年M月D日より、〇〇が△△から▽▽へと変更になりました。",
            "is_published": False,
            "published_at": "2024-03-01T10:00:00"
        }
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "is_published" in response.json()
    assert "published_at" in response.json()
    assert "created_at" in response.json()


def test_create_news_ABNORMAL_01(client_fixture: TestClient):    
    response = client_fixture.post(
        "/news",
        json={
            "title": "〇〇変更のお知らせ",
            "content": "Y年M月D日より、〇〇が△△から▽▽へと変更になりました。",
            "is_published": False,
            "published_at": "2024"
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input data."

"""ニュース更新"""
def test_update_news_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/news/1",
        json={
            "title": "string",
            "content": "string",
            "is_published": False,
            "published_at": "2024-03-01T10:00:00"
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
            "published_at": "2024-03-01T10:00:00"
        }
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "News not found."

"""ニュースカテゴリ更新"""
def test_update_news_category_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/news/categories/1",
        json={
            "name": "string"
        }
    )

    assert response.status_code == 200
    assert "category" in response.json()
    assert "id" in response.json()["category"]