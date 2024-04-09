from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

"""取得成功パターン"""
def test_progresses_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/mentors/1/progresses"
    )
    
    assert response.status_code == 200
    assert "progress_id" in response.json()["progresses"][0]
    assert "user_id" in response.json()["progresses"][0]
    assert "course_id" in response.json()["progresses"][0]
    assert "section_id" in response.json()["progresses"][0]
    assert "curriculum_id" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]