from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_mentors_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/curriculums/1"
    )

    assert response.status_code == 200
    assert "curriculum_id" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    assert "video_url" in response.json()
    assert "content" in response.json()
    assert "is_test" in response.json()
    assert "display_no" in response.json()


"""取得失敗パターン"""
def test_mentors_02(client_fixture: TestClient):

    response = client_fixture.get(
       "/curriculums/999"
    )

    assert response.status_code == 404


