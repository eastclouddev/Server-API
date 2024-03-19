from fastapi.testclient import TestClient


def test_get_courses_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/courses"
    )

    assert response.status_code == 200
    assert len(response.json()["courses"]) == 3