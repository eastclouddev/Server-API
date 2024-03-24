from fastapi.testclient import TestClient


def test_find_course_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/courses/1"
    )

    assert response.status_code == 200


def test_find_course_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/courses/100"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found."