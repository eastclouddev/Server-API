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