from fastapi.testclient import TestClient

def test_xxx_01(client_fixture: TestClient):
    pass

"""会社情報作成"""

"""会社情報取得"""

"""会社情報一覧取得"""

"""進捗管理一覧"""
def test_find_progress_list_company_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies/1/progresses"
    )
    
    assert response.status_code == 200
    assert "progresses" in response.json()
    assert "progress_id" in response.json()["progresses"][0]
    assert "user_id" in response.json()["progresses"][0]
    assert "course_id" in response.json()["progresses"][0]
    assert "section_id" in response.json()["progresses"][0]
    assert "curriculum_id" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]

# def test_find_progress_list_company_02(client_fixture: TestClient):
    
#     response = client_fixture.get(
#         "/companies/999/progresses"
#     )

#     assert response.status_code == 200
#     assert "progresses" in response.json()
#     assert response.json()["progresses"] == []

"""受講生一覧（法人、法人代行)"""
def test_find_student_list_company_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies/1/users/?role=admin&page=1&limit=2",
    )

    data = response.json()
    assert response.status_code == 200
    assert "users" in response.json()
    assert "user_id" in data["users"][0]
    assert "first_name" in data["users"][0]
    assert "last_name" in data["users"][0]
    assert "email" in data["users"][0]
    assert "role" in data["users"][0]
    assert "last_login" in data["users"][0]

def test_find_student_list_company_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get(
       "/companies/999/users/?role=admin&page=1&limit=2",
    )

    assert response.status_code == 404