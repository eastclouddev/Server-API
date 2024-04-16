from fastapi.testclient import TestClient


def test_find_questions(client_fixture: TestClient):
    response = client_fixture.get(
        "mentors/3/students/questions"
    )

    assert response.status_code == 200
