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

def test_find_questions(client_fixture: TestClient):
    response = client_fixture.get(
        "mentors/3/students/questions"
    )

    assert response.status_code == 200

def test_notification_01(client_fixture: TestClient):

    response = client_fixture.get("/mentors/1/notifications")

    assert response.status_code == 200
    assert "id" in response.json()["notifications"][0]
    assert "from_user_id" in response.json()["notifications"][0]
    assert "from_user_name" in response.json()["notifications"][0]
    assert "content" in response.json()["notifications"][0]
    assert "related_question_id" in response.json()["notifications"][0]
    assert "related_answer_id" in response.json()["notifications"][0]
    assert "related_review_request_id" in response.json()["notifications"][0]
    assert "related_review_response_id" in response.json()["notifications"][0]
    assert "is_read" in response.json()["notifications"][0]
    assert "created_at" in response.json()["notifications"][0]

def test_notification_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/mentors/100/notifications")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"