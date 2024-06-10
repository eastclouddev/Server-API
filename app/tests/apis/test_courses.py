from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

"""コース一覧取得"""
def test_find_course_list_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/courses"
    )

    assert response.status_code == 200

"""コース詳細取得"""
def test_find_course_details_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/courses/1"
    )

    assert response.status_code == 200


def test_find_course_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/courses/100"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found."

"""コース開始"""
def test_courses_start_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/start/",
        json={
            "user_id": 11,
            "course_ids": [1, 2, 3]
        }
    )

    assert response.status_code == 201
    assert "courses" in response.json()
    assert "course_id" in response.json()["courses"][0]
    assert "started_at" in response.json()["courses"][0]

def test_courses_start_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/start/",
        json={
            "user_id": 11,
            "course_ids": [100, 200, 300]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Course ID(s) not found."

def test_courses_start_ABNORMAL_02(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/start/",
        json={
            "user_id": "123",
            "course_ids": [100, 200, 300]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Course ID(s) not found."


"""カリキュラムのレビュー一覧"""
def test_find_review_list_01(client_fixture: TestClient):
    response = client_fixture.get("/courses/1/reviews")

    assert response.status_code == 200
    assert "reviews" in response.json()
    assert "id" in response.json()["reviews"][0]
    assert "user" in response.json()["reviews"][0]
    assert "title" in response.json()["reviews"][0]
    assert "content" in response.json()["reviews"][0]
    assert "curriculum_id" in response.json()["reviews"][0]
    assert "created_at" in response.json()["reviews"][0]
    assert "is_read" in response.json()["reviews"][0]
    assert "is_closed" in response.json()["reviews"][0]
    assert "reply_counts" in response.json()["reviews"][0]

def test_find_review_list_02(client_fixture: TestClient):
    response = client_fixture.get("/courses/999/reviews")

    assert response.status_code == 200
    assert "reviews" in response.json()
    assert response.json()["reviews"] == []

"""質問投稿"""
def test_create_question_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/1/questions",
        json={
            "curriculum_id": 1,
            "user_id": 1,
            "title": "title",
            "objective": "objective",
            "current_situation": "current_situation",
            "research": "research",
            "content": "content",
            "media_content": [{"url": "sample1.com"}, {"url": "sample2.com"}]
        }
    )

    assert response.status_code == 201
    assert "question_id" in response.json()
    assert "curriculum_id" in response.json()
    assert "user" in response.json()
    assert "title" in response.json()
    assert "objective" in response.json()
    assert "current_situation" in response.json()
    assert "research" in response.json()
    assert "content" in response.json()
    assert "media_content" in response.json()
    assert "created_at" in response.json()
    assert "is_read" in response.json()
    assert "is_closed" in response.json()
    assert "reply_counts" in response.json()

def test_create_question_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/1/questions",
        json={
            "curriculum_id": 999,
            "user_id": 1,
            "title": "title",
            "objective": "objective",
            "current_situation": "current_situation",
            "research": "research",
            "content": "content",
            "media_content": [{"url": "sample1.com"}, {"url": "sample2.com"}]
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Curriculum not found."

"""レビュー投稿作成"""
def test_create_review_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/1/reviews",
        json={
            "curriculum_id": 1,
            "user_id": 1,
            "title": "string",
            "content": "string",
            "media_content": [{"url": "sample1.com"}, {"url": "sample2.com"}]
        }
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert "user" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "media_content" in response.json()
    assert "created_at" in response.json()
    assert "is_read" in response.json()
    assert "is_closed" in response.json()
    assert "reply_counts" in response.json()

def test_create_review_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/courses/1/reviews",
        json={
            "curriculum_id": 999,
            "user_id": 1,
            "title": "string",
            "content": "string",
            "media_content": [{"url": "sample1.com"}, {"url": "sample2.com"}]
        }
    )

    assert response.status_code == 404

"""カリキュラムの質問一覧"""
def test_find_question_list_in_curriculum_01(client_fixture: TestClient):
    response = client_fixture.get("/courses/1/questions")
    
    assert response.status_code == 200
    assert "question_id" in response.json()["questions"][0]
    assert "curriculum_id" in response.json()["questions"][0]
    assert "user" in response.json()["questions"][0]
    assert "title" in response.json()["questions"][0]
    assert "content" in response.json()["questions"][0]
    assert "created_at" in response.json()["questions"][0]
    assert "is_read" in response.json()["questions"][0]
    assert "is_closed" in response.json()["questions"][0]
    assert "reply_counts" in response.json()["questions"][0]

def test_find_question_list_in_curriculum_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/courses/123/questions")

    assert response.status_code == 404
    assert response.json()["detail"] == "Questions not found for the specified curriculum."
