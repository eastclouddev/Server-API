from logging import getLogger
from typing import Annotated
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.notifications import ListResponseBody
from cruds import notifications as notifications_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("",response_model=ListResponseBody, status_code=status.HTTP_200_OK)
async def find_notification(db: DbDependency):

    """
    通知一覧(管理者)
    
    Parameters
    -----------------------
    
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
    related_review_respomse_id: int
        レビューリスポンスのID
    is_read: bool
        通知が既読かどうか
    created_at: str
    """

    user = notifications_crud.find_user(db)

    # if not user:
    #     raise HTTPException(status_code=404, detail="")

    questions = notifications_crud.find_questions(db)

    review_requests = notifications_crud.find_reviews(db)

    li = []
    count = 1
    for question in questions:
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.first_name + user.last_name,
            "content": question.content,
            "related_question_id": question.id,
            "related_answer_id": None,
            "related_review_request_id": None,
            "related_review_response_id": None,
            "is_read": True,#TODO:db追加
            "created_at": question.created_at.isoformat()
        }
        li.append(di)
        count = count + 1
        answers = notifications_crud.find_answers(db)
        for answer in answers:
            di = {
                "id": count,
                "from_user_id": user.id,
                "from_user_name": user.first_name + user.last_name,
                "content": answer.content,
                "related_question_id": question.id,
                "related_answer_id": answer.id,
                "related_review_request_id": None,
                "related_review_response_id": None,
                "is_read": answer.is_read,
                "created_at": answer.created_at.isoformat()
            }
            li.append(di)
            count = count +1

    for review_request in review_requests:
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.first_name + user.last_name,
            "content": review_request.content,
            "related_question_id": None,
            "related_answer_id": None,
            "related_review_request_id": review_request.id,
            "related_review_response_id": None,
            "is_read": True,#TODO:db追加
            "created_at": review_request.created_at.isoformat()
        }
        li.append(di)
        count = count + 1
        review_responses = notifications_crud.find_is_read(db)
        for  review_response in review_responses:
            di = {
                "id": count,
                "from_user_id": user.id,
                "from_user_name": user.first_name + user.last_name,
                "content": review_response.content,
                "related_question_id": None,
                "related_answer_id": None,
                "related_review_request_id": review_request.id,
                "related_review_response_id": review_response.id,
                "is_read": review_response.is_read,
                "created_at": review_response.created_at.isoformat()
            }
            li.append(di)
            count = count +1

    return {"notifications": li}