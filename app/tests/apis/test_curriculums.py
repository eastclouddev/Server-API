from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

def test_curriculums_01(client_fixture: TestClient):

    response = client_fixture.get("/curriculums/1/questions")
    
    assert response.status_code == 200
    assert "question_id" in response.json()["questions"][0]
    assert "curriculum_id" in response.json()["questions"][0]
    assert "user_id" in response.json()["questions"][0]
    assert "title" in response.json()["questions"][0]
    assert "content" in response.json()["questions"][0]
    assert "media_content" in response.json()["questions"][0]
    assert "url" in response.json()["questions"][0]["media_content"][0]

def test_curriculums_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/curriculums/123/questions")

    assert response.status_code == 404
    assert response.json()["detail"] == "Questions not found for the specified curriculum."