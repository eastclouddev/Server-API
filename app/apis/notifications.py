from logging import getLogger
from typing import Annotated
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.notifications import NotificationListResponseBody, NotificationUpdateResponseBody
from cruds import notifications as notifications_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=NotificationListResponseBody, status_code=status.HTTP_200_OK)
async def find_notification(db: DbDependency):

    """
    通知一覧(管理者)
    
    Parameters
    -----------------------
    なし
    
    -----------------------
    id: int
        通知のID
    from_user_id: int
        ユーザーのID
    from_user_name: str
        ユーザーの名前
    content: str
        通知の内容
    related_question_id: int
        質問のID
    related_answer_id: int
        回答のID
    related_review_request_id: int
        レビューリクエストのID
    related_review_response_id: int
        レビューレスポンスのID
    is_read: bool
        通知が既読かどうか
    created_at: str
        作成日時
    """
    
    # 4つの各テーブルから取得
    all_tables = notifications_crud.find_table(db)
    li = []
    for all_table in all_tables:
        di = {
            "id": all_table[0],
            "content": all_table[1],
            "created_at": all_table[2]
        }
        li.append(di)

    # 作成日が新しい順に並び替える
    re_sorted = sorted(li, key=lambda x:x["created_at"], reverse=True)
    # 並び替えたものから先頭10件取得
    re_sorted = re_sorted[:10]
    count = 1
    li = []

    for r in re_sorted:
        table, data = notifications_crud.find_db(db, r["id"], r["content"], r["created_at"])
        # ユーザー取得
        user = notifications_crud.find_user_by_id(db, data.user_id)
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.last_name + user.first_name,
            "content": data.content,
            "related_question_id": data.id if table == "question" else data.question_id if table == "answer" else None,
            "related_answer_id": data.id if table == "answer" else None,
            "related_review_request_id": data.id if table == "request" else data.review_request_id if table == "response" else None,
            "related_review_response_id": data.id if table == "response" else None,
            "is_read": data.is_read,
            "created_at": data.created_at.isoformat()
        }
        li.append(di)
        count += 1

    return {"notifications": li}

@router.patch("/{notification_id}/mark_read", response_model=NotificationUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_notification(db: DbDependency, notification_id: int):

    """
    通知内容を既読に更新
    
    Parameters
    -----------------------
    notification_id: int
        既読にする通知のID
    
    -----------------------
    mesasge: str
        操作成功のメッセージ(固定値:Notification marked as read successfully.)
    notification_id: int
        既読にした通知のID
    """

    try:
        notification = notifications_crud.update_notificaton_by_id(db, notification_id)
        if not notification:
            raise Exception("Notification not found")
        db.commit()
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=404, detail="Notification ID not found.")


    return {"message": "Notification marked as read successfully.", "notification_id": notification_id}