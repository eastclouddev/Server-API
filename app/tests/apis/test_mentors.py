from fastapi.testclient import TestClient


def test_find_by_mentor_id_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/mentors/1/rewards"
    )

    assert response.status_code == 200
    assert "rewards" in response.json()
    assert len(response.json()["rewards"]) == 3


def test_find_by_mentor_id_02(client_fixture: TestClient):
    response = client_fixture.get(
        "mentors/2/rewards"
    )

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Mentor not found."