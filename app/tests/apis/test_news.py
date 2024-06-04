from datetime import datetime

from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass


"""ニュース詳細取得"""
def test_find_news_details_01(client_fixture: TestClient):
    response = client_fixture.get("/news/1/")

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "category" in response.json()
    assert "published_at" in response.json()

def test_find_news_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/news/999/")

    assert response.status_code == 404
    assert response.json()["detail"] == "The requested news article was not found."

"""ニュース一覧(管理者)取得"""
def test_find_news_list_01(client_fixture: TestClient):
    response = client_fixture.get("/news/?page=1&limit=2")
    assert response.status_code == 200
    assert "id" in response.json()["news"][0]
    assert "title" in response.json()["news"][0]
    assert "category" in response.json()["news"][0]
    assert "published_at" in response.json()["news"][0]

"""ニュース作成"""
def test_create_news_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/news",
        json={
            "title": "Newsのタイトル",
            "content": "Newsの内容",
            "category_id": "1",
            "published_at": "2024-03-01T10:00:00"
        }
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "category_id" in response.json()
    assert "is_published" in response.json()
    assert "published_at" in response.json()
    assert "created_at" in response.json()


def test_create_news_ABNORMAL_01(client_fixture: TestClient):    
    response = client_fixture.post(
        "/news",
        json={
            "title": "〇〇変更のお知らせ",
            "content": "Y年M月D日より、〇〇が△△から▽▽へと変更になりました。",
            "category_id": "4",
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
            "category_id": "1",
            "is_published": True,
            "published_at": "2024-03-01T10:00:00Z"
        }
    )

    assert response.status_code == 200
    assert "news_id" in response.json()
    assert "title" in  response.json()
    assert "content" in response.json()
    assert "category_id" in response.json()
    assert "is_published" in response.json()
    assert "published_at" in response.json()
    assert "updated_at" in response.json()

def test_update_news_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch(
        "/news/123",
        json={
            "title": "string",
            "content": "string",
            "category_id": "1",
            "is_published": False,
            "published_at": "2024-03-01T10:00:00Z"
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

"""ニュースカテゴリ作成"""
def test_news_category_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/news/categories",
        json={
            "name": "string"
        }
    )

    assert response.status_code == 201
    assert "category" in response.json()
    assert "id" in response.json()["category"]

"""ニュースカテゴリ一覧取得"""
def test_find_news_category_list_01(client_fixture: TestClient):
    response = client_fixture.get("/news/categories/")

    assert response.status_code == 200
    assert "categories" in response.json()
    assert "id" in response.json()["categories"][0]
    assert "name" in response.json()["categories"][0]
    assert "created_at" in response.json()["categories"][0]
    assert "updated_at" in response.json()["categories"][0]

"""ニュース一覧取得"""
def test_find_news_list_02(client_fixture: TestClient):
    response = client_fixture.get("/news/published?page=1&limit=2")

    assert response.status_code == 200
    assert "id" in response.json()["news"][0]
    assert "title" in response.json()["news"][0]
    assert "category" in response.json()["news"][0]
    assert "published_at" in response.json()["news"][0]