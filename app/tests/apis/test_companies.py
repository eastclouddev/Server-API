from fastapi.testclient import TestClient

def test_xxx_01(client_fixture: TestClient):
    pass

"""会社情報作成"""
def test_create_company_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/companies",
        json={
            "name": "A社",
            "prefecture": "A都",
            "city": "A区",
            "town": "A町",
            "address": "建物A",
            "postal_code": "000-0000",
            "phone_number": "000-0000-0000",
            "email": "aaa@mail.com"
        }
    )
    assert response.status_code == 200
    assert "company_id" in response.json()
    assert "name" in response.json()
    assert "prefecture" in response.json()
    assert "city" in response.json()
    assert "town" in response.json()
    assert "address" in response.json()
    assert "postal_code" in response.json()
    assert "phone_number" in response.json()
    assert "email" in response.json()

def test_create_company_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
        "/companies",
        json={
            "name": 123,
            "prefecture": "A都",
            "city": "A区",
            "town": "A町",
            "address": "建物A",
            "postal_code": "000-0000",
            "phone_number": "000-0000-0000",
            "email": "aaa@mail.com"
        }
    )
    assert response.status_code == 422

"""会社情報詳細"""
def test_find_company_details_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies/1"
    )

    assert response.status_code == 200
    assert "company_id" in response.json()
    assert "name" in response.json()
    assert "prefecture" in response.json()
    assert "city" in response.json()
    assert "town" in response.json()
    assert "address" in response.json()
    assert "postal_code" in response.json()
    assert "phone_number" in response.json()
    assert "email" in response.json()
    assert "created_at" in response.json()
    assert "updated_at" in response.json()

def test_find_company_details_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get(
       "/companies/999"
    )

    assert response.status_code == 404

"""会社情報一覧取得"""
def test_find_company_list_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies"
    )

    assert response.status_code == 200
    assert "company_id" in response.json()["companies"][0]
    assert "name" in response.json()["companies"][0]
    assert "prefecture" in response.json()["companies"][0]
    assert "city" in response.json()["companies"][0]
    assert "town" in response.json()["companies"][0]
    assert "address" in response.json()["companies"][0]
    assert "postal_code" in response.json()["companies"][0]
    assert "phone_number" in response.json()["companies"][0]
    assert "email" in response.json()["companies"][0]
    assert "created_at" in response.json()["companies"][0]

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

def test_find_progress_list_company_02(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/companies/999/progresses"
    )

    assert response.status_code == 200
    assert "progresses" in response.json()
    assert response.json()["progresses"] == []

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

"""請求履歴一覧取得"""
def test_find_billing_list_01(client_fixture: TestClient):
    
    response = client_fixture.get("/companies/3/billings")

    assert response.status_code == 200
    assert "billing_id" in response.json()["billings"][0]
    assert "date" in response.json()["billings"][0]
    assert "amount" in response.json()["billings"][0]
    assert "status" in response.json()["billings"][0]
    assert "description" in response.json()["billings"][0]

def test_find_billing_list_ABNORMAL_01(client_fixture: TestClient):

    response = client_fixture.get("/companies/999/billings")

    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found."

"""有効アカウント数取得"""
def test_find_number_of_accounts_01(client_fixture: TestClient):
    response = client_fixture.get("/companies/1/users/counts/")

    assert response.status_code == 200
    assert "company_id" in response.json()
    assert "role_counts" in response.json()

def test_find_number_of_accounts_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/companies/111/users/counts/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found."