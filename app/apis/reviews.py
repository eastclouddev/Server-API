from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query,Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.reviews import UpdateResponseRequestBody, UpdateResponseResponseBody, UpdateReviewRequestBody, UpdateReviewResponseBody,AllResponseBody

from cruds import reviews as reviews_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.patch("/responses/{response_id}", response_model=UpdateResponseResponseBody, status_code=status.HTTP_200_OK)
async def update_review_response(db: DbDependency, update: UpdateResponseRequestBody, response_id: int = Path(gt=0)):
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
    
    new_response = reviews_crud.update_response(db, update,response_id)
    if not new_response:
        raise HTTPException(status_code=404, detail="Response not found.")

    try:
        db.commit()
        return new_response

    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")


@router.patch("/{review_id}", response_model=UpdateReviewResponseBody, status_code=status.HTTP_200_OK)
async def update_review(db: DbDependency, update: UpdateReviewRequestBody, review_id: int = Path(gt=0)):
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
    
    new_review = reviews_crud.update_review(db, update,review_id)
    if not new_review:
        raise HTTPException(status_code=404, detail="Curriculum not found.")

    try:
        db.commit()
        return new_review

    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")


@router.get("/{mentor_id}/students/reviews",response_model= AllResponseBody,status_code=status.HTTP_200_OK)
async def get_all_reviews(request: Request,db: DbDependency, mentor_id: int):
    """
    受講生のレビュー一覧取得
    
    Parameters
    ----------
    user_id

    Returns
    -------
    {"reviews": reviews_list} : dic{}
                    レビュー一覧
    
    """
    found_reviews = reviews_crud.find_reviews(db,mentor_id)


    reviews_list = []

    for review in found_reviews:
        one_review = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "created_at": review.created_at.isoformat(),
            "is_read": reviews_crud.find_is_read(db,review.id),
            "is_closed": review.is_closed
        }

        reviews_list.append(one_review)

    return {"reviews": reviews_list} 

