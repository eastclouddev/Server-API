from fastapi.testclient import TestClient

"""進捗管理一覧"""
def test_progresses_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/progresses"
    )
    
    assert response.status_code == 200
    assert "user_id" in response.json()["progresses"][0]
    assert "user_name" in response.json()["progresses"][0]
    assert "course_id" in response.json()["progresses"][0]
    assert "course_name" in response.json()["progresses"][0]
    assert "section_id" in response.json()["progresses"][0]
    assert "curriculum_id" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]






