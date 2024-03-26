from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.reviews import CreateRequestBody, CreateResponseBody, RequestBody, ResponseBody
from cruds import reviews as reviews_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/{review_request_id}/responses", response_model=CreateResponseBody, status_code=status.HTTP_200_OK)
async def create_review_response(db: DbDependency, param: CreateRequestBody, review_request_id: int):
    
    new_review_response = reviews_crud.create_review_response(db, param, review_request_id)

    if not new_review_response:
        raise HTTPException(status_code=404, detail="Review request not found.")
    
    try:
        db.commit()

        re_di = {
          "id": new_review_response.id,
          "review_request_id": new_review_response.review_request_id,
          "user_id": new_review_response.user_id,
          "parent_response_id": new_review_response.parent_response_id,
          "content": new_review_response.content,
          "is_read": new_review_response.is_read,
          "created_at": new_review_response.created_at.isoformat()
        }

        return re_di

    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")


@router.patch("/responses/{response_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def update_review_response(db: DbDependency, update: RequestBody, response_id: int = Path(gt=0)):
    """
    レビュー回答更新

    Parameter
    -----------------------
    response_id: int
        更新したい回答のID
    content: text
		回答の更新された内容
    is_read: bool
		回答が既読かどうかを更新するフラグ

    Return
    ----------------------
    id: int
		更新された回答のID
    review_request_id: int
		回答が紐づくレビューリクエストのID
    user_id: int
		回答を投稿したユーザーのID
    parent_response_id: int
		返信先の回答ID
    content: text
		更新された回答の内容
    is_read: bool
		回答が既読かどうかを示すフラグ
    updated_at: str
		回答が最後に更新された日時

    """
    
    new_response = reviews_crud.update(db, update,response_id)
    if not new_response:
        raise HTTPException(status_code=404, detail="Response not found.")
    try:
        db.commit()
    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    return new_response