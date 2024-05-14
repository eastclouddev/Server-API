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