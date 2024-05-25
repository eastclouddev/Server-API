from fastapi.testclient import TestClient

def test_notification_01(client_fixture: TestClient):
    pass 
    # sqlite3ではUNION_ALLが使えないため

    # response = client_fixture.get("/notifications")

    # assert response.status_code == 200
    # assert "id" in response.json()["notifications"][0]
    # assert "from_user_id" in response.json()["notifications"][0]
    # assert "from_user_name" in response.json()["notifications"][0]
    # assert "content" in response.json()["notifications"][0]
    # assert "related_question_id" in response.json()["notifications"][0]
    # assert "related_answer_id" in response.json()["notifications"][0]
    # assert "related_review_request_id" in response.json()["notifications"][0]
    # assert "related_review_response_id" in response.json()["notifications"][0]
    # assert "is_read" in response.json()["notifications"][0]
    # assert "created_at" in response.json()["notifications"][0]


def test_update_notification_01(client_fixture: TestClient):
    response = client_fixture.patch("/notifications/1/mark_read")

    assert response.status_code == 200
    assert "message" in response.json()
    assert "notification_id" in response.json()
    assert response.json()["message"] == "Notification marked as read successfully."
    assert response.json()["notification_id"] == 1

def test_update_notification_ABNORMAL_01(client_fixture: TestClient):
    response = client_fixture.patch("/notifications/123/mark_read")

    assert response.status_code == 404
    assert response.json()["detail"] == "Notification ID not found."