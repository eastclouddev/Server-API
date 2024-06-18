from fastapi.testclient import TestClient


"""カリキュラム詳細取得"""
def test_find_curriculum_details_01(client_fixture: TestClient):
    response = client_fixture.get("/curriculums/1")

    assert response.status_code == 200
    assert "curriculum_id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "video_url" in response.json()
    assert "content" in response.json()
    assert "is_quiz" in response.json()
    assert "quiz_content" in response.json()
    assert "display_no" in response.json()

def test_find_curriculum_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/curriculums/999")

    assert response.status_code == 404
