from fastapi.testclient import TestClient

def test_find_all_01(client_fixture: TestClient):
    response = client_fixture.get("/news/?page=1&limit=2")
    assert response.status_code == 200
    assert "id" in response.json()["news"][0]
    assert "title" in response.json()["news"][0]
    assert "published_at" in response.json()["news"][0]
    assert "page" in response.json()
    assert "limit" in response.json()
    assert "total_pages" in response.json()
    assert "total_news" in response.json()

