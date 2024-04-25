from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

# TODO:↓名前変わるかも
"""自分の質問を取得する"""
def test_students_01(client_fixture: TestClient):
    response = client_fixture.get("/students/1/questions")

    assert response.status_code == 200
    assert "id" in response.json()["questions"][0]
    assert "title" in response.json()["questions"][0]
    assert "content" in response.json()["questions"][0]
    assert "curriculum_id" in response.json()["questions"][0]
    assert "created_at" in response.json()["questions"][0]
    assert "is_read" in response.json()["questions"][0]
    assert "is_closed" in response.json()["questions"][0]

def test_students_02(client_fixture: TestClient):
    response = client_fixture.get("/students/999/questions")

    assert response.status_code == 404
    assert response.json()["detail"] == "question not found"

# TODO:↓名前変わるかも
"""現在の学習進捗"""
def test_find_progress_list_student_01(client_fixture: TestClient):
    response = client_fixture.get("students/1/progresses")
    assert response.status_code == 200
    assert "course_id" in response.json()["progresses"][0]
    assert "course_title" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]
    assert "status" in response.json()["progresses"][0]
    assert "last_accessed_at" in response.json()["progresses"][0]

"""自分のレビュー一覧取得"""
def test_find_my_review_list_01(client_fixture: TestClient):

    response = client_fixture.get("/students/3/reviews")
    
    assert response.status_code == 200
    assert "id" in response.json()["reviews"][0]
    assert "title" in response.json()["reviews"][0]
    assert "content" in response.json()["reviews"][0]
    assert "curriculum_id" in response.json()["reviews"][0]
    assert "created_at" in response.json()["reviews"][0]
    assert "is_read" in response.json()["reviews"][0]
    assert "is_closed" in response.json()["reviews"][0]

def test_find_my_review_list_02(client_fixture: TestClient):

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
    