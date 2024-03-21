from fastapi.testclient import TestClient

"""送金先作成"""
"""成功パターン"""
def test_mentors_01(client_fixture: TestClient):

    response = client_fixture.post(
       "/mentors/5/accounts",
       json={
            "bank_name": "Aバンク",
            "branch_name": "A支店",
            "bank_code": "123" ,
            "branch_code": "456",
            "account_type": "普通", 
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


"""失敗パターン"""
def test_mentors_02(client_fixture: TestClient):

    response = client_fixture.post(
       "/mentors/112/accounts",
        json={
            "bank_name": "Aバンク",
            "branch_name": "A支店",
            "bank_code": "123" ,
            "branch_code": "456",
            "account_type": "普通", 
            "account_number": "11-22-33",
            "account_name": "A太郎",
        }  
    )

    assert response.status_code == 404