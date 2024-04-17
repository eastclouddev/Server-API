from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

def test_find_all_01(client_fixture: TestClient):
    response = client_fixture.get("students/1/progresses")
    assert response.status_code == 200
    assert "course_id" in response.json()["progresses"][0]
    assert "course_title" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]
    assert "status" in response.json()["progresses"][0]
    assert "last_accessed_at" in response.json()["progresses"][0]

def test_my_student_01(client_fixture: TestClient):

    response = client_fixture.get("/students/3/reviews")
    
    assert response.status_code == 200
    assert "id" in response.json()["reviews"][0]
    assert "title" in response.json()["reviews"][0]
    assert "content" in response.json()["reviews"][0]
    assert "curriculum_id" in response.json()["reviews"][0]
    assert "created_at" in response.json()["reviews"][0]
    assert "is_read" in response.json()["reviews"][0]
    assert "is_closed" in response.json()["reviews"][0]

def test_my_student_02(client_fixture: TestClient):

    response = client_fixture.get("/students/100/reviews")

    assert response.status_code == 200
    assert response.json()["reviews"] == []