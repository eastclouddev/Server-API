from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.reviews import RequestBody,ResponseBody
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import reviews as review_crud
from logging import getLogger

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/reviews", tags=["ReviewResponses"])


@router.patch("/responses/{response_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def response_update(db: DbDependency, update: RequestBody,response_id: int = Path(gt=0)):
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
    
    new_response = review_crud.update(db, update,response_id)
    if not new_response:
        raise HTTPException(status_code=404, detail="Response not found.")
    try:
        db.commit()
    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    return new_response