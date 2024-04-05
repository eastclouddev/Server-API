from fastapi.testclient import TestClient


def test_xxx_01(client_fixture: TestClient):
    pass

def test_find_test_details_01(client_fixture: TestClient):
    response = client_fixture.get(
        "curriculums/1/test"
    )
    assert response.status_code == 200
    assert "curriculum_id" in response.json()
    assert "tests" in response.json()
    assert "test_id" in response.json()["tests"][0]
    assert "question" in response.json()["tests"][0]
    assert "options" in response.json()["tests"][0]
    assert "correct_answer" in response.json()["tests"][0]
    assert "explanation" in response.json()["tests"][0]
    assert "media_content_url" in response.json()["tests"][0]
def test_find_test_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get(
        "curriculums/100/test"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Test content not found for the specified curriculum."














