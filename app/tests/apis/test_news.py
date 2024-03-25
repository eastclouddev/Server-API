from datetime import datetime

from fastapi.testclient import TestClient


# def test_create_news_01(client_fixture: TestClient):
#     # sqliteでは文字列を日付型に入れることができない
#     published_at = datetime.strptime("2024-03-01T10:00:00", "%Y-%m-%dT%H:%M:%S")
#     published_at = "2024-03-01T10:00:00"
    
#     response = client_fixture.post(
#         "/news",
#         json={
#             "title": "〇〇変更のお知らせ",
#             "content": "Y年M月D日より、〇〇が△△から▽▽へと変更になりました。",
#             "is_published": False,
#             "published_at": "2024-03-01T10:00:00"
#         }
#     )

#     assert response.json()["detail"] == "Invalid input data."
#     assert response.status_code == 201
#     assert "id" in response.json()
#     assert "title" in response.json()
#     assert "content" in response.json()
#     assert "is_published" in response.json()
#     assert "published_at" in response.json()
#     assert "created_at" in response.json()


def test_create_news_ABNORMAL_01(client_fixture: TestClient):    
    response = client_fixture.post(
        "/news",
        json={
            "title": "〇〇変更のお知らせ",
            "content": "Y年M月D日より、〇〇が△△から▽▽へと変更になりました。",
            "is_published": False,
            "published_at": "2024-03-01T10:00:00"
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input data."