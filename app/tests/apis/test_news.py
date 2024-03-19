from fastapi.testclient import TestClient


def test_find_by_news_id_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/news/1"
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "summary" in response.json()
    assert "content" in response.json()
    assert "published_at" in response.json()

def test_find_by_news_id_02(client_fixture: TestClient):
    response = client_fixture.get(
        "/news/100"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "The requested news article was not found."