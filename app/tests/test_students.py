from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_students_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/students/1/questions"
    )

    assert response.status_code == 200
    assert "id" in response.json()["questions"][0]
    assert "title" in response.json()["questions"][0]
    assert "content" in response.json()["questions"][0]
    assert "curriculum_id" in response.json()["questions"][0]
    assert "created_at" in response.json()["questions"][0]
    assert "is_read" in response.json()["questions"][0]
    assert "is_closed" in response.json()["questions"][0]



"""取得失敗パターン"""
def test_students_02(client_fixture: TestClient):

    response = client_fixture.get(
       "/students/999/questions"
    )

    assert response.status_code == 404

