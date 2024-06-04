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
    dict: array
        id: int
            通知のID
        from_user: dict
            id: int
                ユーザーのID
            name: str
                ユーザーの名前
        question_id: int
            質問のID
        answer_id: int
            回答のID
        related_review_request_id: int
            レビューリクエストのID
        related_review_response_id: int
            レビューレスポンスのID
        title: str
            通知のタイトル
        content: str
            通知の内容
        is_read: bool
            通知が既読かどうか
        created_at: str
            通知が生成された日時（ISO 8601形式）
    """

    notifications = notifications_crud.find_notifications_order_by_created_at(db)
    li = []

    for i, notification in enumerate(notifications):
        q_id = None
        a_id = None
        req_id = None
        res_id = None        
        title = ""
        content = ""
        if notification.question_id:
            question = notifications_crud.find_question_by_question_id(db, notification.question_id)
            q_id = question.id
            title = question.title
            content = question.content
        elif notification.answer_id:
            answer = notifications_crud.find_answer_by_answer_id(db, notification.answer_id)
            q_id = answer.question_id
            a_id = answer.id
            question = notifications_crud.find_question_by_question_id(db, answer.question_id)
            title = question.title
            content = answer.content
        # レビューリクエスト・レビューレスポンス
        elif notification.review_request_id:
            request = notifications_crud.find_request_by_request_id(db, notification.review_request_id)
            req_id = request.id
            title = request.title
            content = request.content
        elif notification.review_response_id:
            response = notifications_crud.find_response_by_response_id(db, notification.review_response_id)
            req_id = response.review_request_id
            res_id = response.id
            request = notifications_crud.find_request_by_request_id(db, response.review_request_id)
            title = request.title
            content = response.content

        user = notifications_crud.find_user_by_id(db, notification.user_id)

        di = {
            "id": i + 1,
            "from_user": {
                "id": notification.user_id,
                "name": user.last_name + user.first_name
            },
            "question_id": q_id,
            "answer_id": a_id,
            "review_request_id": req_id,
            "review_response_id": res_id,
            "title": title,
            "content": content,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat()
        }
        li.append(di)

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