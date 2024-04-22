from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

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

def test_notification_01(client_fixture: TestClient):

    response = client_fixture.get("/students/3/notifications")
    
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

    response = client_fixture.get("/students/100/notifications")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    