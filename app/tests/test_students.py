from fastapi.testclient import TestClient

"""取得成功パターン"""
def test_students_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/students/1/questions"
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "title" in response.json()
    assert "content" in response.json()
    assert "curriculum_id" in response.json()
    assert "created_at" in response.json()
    assert "is_read" in response.json()
    assert "is_closed" in response.json()



"""取得失敗パターン"""
def test_students_02(client_fixture: TestClient):

    response = client_fixture.get(
       "/students/999/questions"
    )

    assert response.status_code == 404


