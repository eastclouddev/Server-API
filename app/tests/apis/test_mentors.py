from fastapi.testclient import TestClient

def test_xxx_01(client_fixture: TestClient):
    pass

"""送金履歴一覧"""
def test_find_reward_list_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/mentors/1/rewards"
    )

    assert response.status_code == 200
    assert "rewards" in response.json()

def test_find_reward_list_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get(
        "mentors/999/rewards"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Mentor not found."

"""送金先情報詳細"""
def test_find_account_info_details_01(client_fixture: TestClient):
    response = client_fixture.get("/mentors/6/accounts")

    assert response.status_code == 200
    assert "mentor_id" in response.json()
    assert "account_name" in response.json()
    assert "bank_name" in response.json()
    assert "branch_name" in response.json()
    assert "account_number" in response.json()
    assert "account_type" in response.json()

def test_find_account_info_details_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.get("/mentors/999/accounts")

    assert response.status_code == 404
    assert response.json()["detail"] == "Mentor not found."

"""送金先情報作成"""
def test_create_account_info_01(client_fixture: TestClient):
    response = client_fixture.post(
       "/mentors/6/accounts",
       json={
            "bank_name": "Aバンク",
            "branch_name": "A支店",
            "bank_code": "123" ,
            "branch_code": "456",
            "account_type": "ordinary", 
            "account_number": "11-22-33",
            "account_name": "A太郎",
        }
    )

    assert response.status_code == 201
    assert "account_id" in response.json()
    assert "mentor_id" in response.json()
    assert "bank_name" in response.json()
    assert "branch_name" in response.json()
    assert "bank_code" in response.json()
    assert "branch_code" in response.json()
    assert "account_type" in response.json()
    assert "account_number" in response.json()
    assert "account_name" in response.json()

def test_create_account_info_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.post(
       "/mentors/999/accounts",
        json={
            "bank_name": "Aバンク",
            "branch_name": "A支店",
            "bank_code": "123" ,
            "branch_code": "456",
            "account_type": "ordinary", 
            "account_number": "11-22-33",
            "account_name": "A太郎",
        }  
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Mentor not found."

"""進捗管理一覧"""
def test_progresses_01(client_fixture: TestClient):
    
    response = client_fixture.get(
        "/mentors/1/progresses"
    )
    
    assert response.status_code == 200
    assert "progress_id" in response.json()["progresses"][0]
    assert "user_id" in response.json()["progresses"][0]
    assert "course_id" in response.json()["progresses"][0]
    assert "section_id" in response.json()["progresses"][0]
    assert "curriculum_id" in response.json()["progresses"][0]
    assert "progress_percentage" in response.json()["progresses"][0]


"""受講生からの質問一覧取得"""
def test_find_question_list_from_student_01(client_fixture: TestClient):
    response = client_fixture.get(
        "mentors/3/students/questions"
    )

    assert response.status_code == 200

"""受講生のレビュー一覧取得"""
def test_find_review_list_from_student_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/mentors/6/students/reviews"
    )
    
    assert response.status_code == 200
    assert "id" in response.json()["reviews"][0]
    assert "title" in response.json()["reviews"][0]
    assert "content" in response.json()["reviews"][0]
    assert "curriculum_id" in response.json()["reviews"][0]
    assert "created_at" in response.json()["reviews"][0]
    assert "is_read" in response.json()["reviews"][0]
    assert "is_closed" in response.json()["reviews"][0]

"""メンター担当受講者数取得"""
def test_find_mentors_student_count_01(client_fixture: TestClient):
    response = client_fixture.get(
        "/mentors/counts"
    )
    
    assert response.status_code == 200
    assert "mentor_id" in response.json()["mentors"][0]
    assert "mentor_name" in response.json()["mentors"][0]
    assert "student_count" in response.json()["mentors"][0]