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
router = APIRouter(prefix="/reviews", tags=["ReviewRequest"])


@router.patch("/{review_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def review_update(db: DbDependency, update: RequestBody,review_id: int = Path(gt=0)):
    """
    レビュー更新

    Parameter
    -----------------------
    review_id: int
        更新したいレビューのID
    title: str
        レビューリクエストのタイトル
    content: str
		レビューの更新された内容
    is_read: bool
		レビューが既読かどうかを更新するフラグ

    Return
    ----------------------
    id: int
		更新されたレビューリクエストのID
    title: str
        レビューリクエストのタイトル
    content: text
		更新されたレビューの内容
    is_read: bool
		レビューが既読かどうかを示すフラグ
    updated_at: str
		レビューが最後に更新された日時

    """
    
    new_review = review_crud.update(db, update,review_id)
    if not new_review:
        raise HTTPException(status_code=404, detail="Curriculum not found.")
    try:
        db.commit()
    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    return new_review