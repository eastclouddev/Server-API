# from fastapi.testclient import TestClient


# def test_find_all_01(client_fixture: TestClient):
#     response = client_fixture.get("/products")
#     assert response.status_code == 200
#     products = response.json()
#     assert len(products) == 2

# # Abnormal 01: id not-found
# def test_find_by_id_ABNORMAL_01(client_fixture: TestClient):
#     response = client_fixture.get("/products/10")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Product not found"

from fastapi.testclient import TestClient


def get_user_01(client_fixture: TestClient):

    response = client_fixture.get(
        "/companies/{company_id}/users",

    role = "student",
    page = 1,
    limit = 3

    )

    data = response.json()


    assert response.status_code == 200
    assert "users" in response.json()
    assert data["users"] 

    data = data[0]

    assert "user_id" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "email" in data
    assert "role" in data
    assert "last_login" in data
    

