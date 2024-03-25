from fastapi.testclient import TestClient

def test_find_all_01(client_fixture: TestClient):
    response = client_fixture.get("/state_progresses")
    assert response.status_code == 200
    assert "course_id" in response.json()["progresses"][0]
    assert "course_title" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]
    assert "status" in response.json()["progresses"][0]
    assert "last_accessed_at" in response.json()["progresses"][0]
    
# def test_find_by_id_ABNORMAL_01(client_fixture: TestClient):
#      response = client_fixture.get("/state_progresses")
#      assert response.status_code == 401
#      assert response.json()["detail"] == "Unauthoried access. Please log in."