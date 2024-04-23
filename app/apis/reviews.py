from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query,Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.reviews import UpdateResponseRequestBody, UpdateResponseResponseBody, UpdateReviewRequestBody, UpdateReviewResponseBody, \
    AllResponseBody, AllReviewResponse

from cruds import reviews as reviews_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.patch("/responses/{response_id}", response_model=UpdateResponseResponseBody, status_code=status.HTTP_200_OK)
async def update_review_response(db: DbDependency, update: UpdateResponseRequestBody, response_id: int = Path(gt=0)):
    """
    レビュー回答更新

    Parameters
    -----------------------
    dict
        response_id: int
            更新したい回答のID
        content: str
            回答の更新された内容
        is_read: bool
            回答が既読かどうかを更新するフラグ

    Returns
    -----------------------
    dict
        id: int
            更新された回答のID
        review_request_id: int
            回答が紐づくレビューリクエストのID
        user_id: int
            回答を投稿したユーザーのID
        parent_response_id: int
            返信先の回答ID
        content: str
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
async def update_review_request(db: DbDependency, update: UpdateReviewRequestBody, review_id: int = Path(gt=0)):
    """
    レビュー更新（受講生）

    Parameters
    -----------------------
    dict
        review_id: int
            更新したいレビューのID
        title: str
            レビューリクエストのタイトル
        content: str
            レビューの更新された内容
        is_read: bool
            レビューが既読かどうかを更新するフラグ

    Returns
    -----------------------
    dict
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

# TODO:記述するファイル違くない？
@router.get("/{mentor_id}/students/reviews",response_model= AllResponseBody,status_code=status.HTTP_200_OK)
async def find_review_list_from_student(request: Request,db: DbDependency, mentor_id: int):
    """
    受講生のレビュー一覧取得
    
    Parameter
    -----------------------
    mentor_id: int
        取得するメンターのユーザーID

    Returns
    -----------------------
    reviews: array
        id: int
            レビューのID
        title: str
            レビューのタイトル
        content: str
            レビューの内容
        curriculum_id: int
            レビューに紐づくカリキュラムのID
        created_at:str
            レビューの作成日（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
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

@router.get("/{review_request_id}", response_model=AllReviewResponse, status_code=status.HTTP_200_OK)
async def find_review_thread_details(db: DbDependency, review_request_id: int):
    """
    レビュースレッド詳細
    
    Parameter
    -----------------------
    dict
        review_request_id: int
            スレッド詳細を取得したいレビューリクエストのID

    Returns
    -----------------------
    dict
        id: int
            レビューリクエストのID
        curriculum_id: int
            関連するカリキュラムのID
        user_id: int
            レビューリクエストを投稿したユーザーのID
        title: str
            レビューリクエストのタイトル
        content: str
            レビューリクエストの内容
        is_closed: bool
            レビューリクエストがクローズされているかどうか
        created_at: str
            レビューリクエストが作成された日時 
        updated_at:str
            レビューリクエストが最後に更新された日時
        id: int
            回答のID
        review_request_id: int
            回答が紐づくレビューリクエストのID
        user_id: int
            回答を投稿したユーザーのID
        parent_response_id: int
            返信先の回答ID
        content: str
            回答の内容
        is_read: bool
            回答が既読かどうかを示すフラグ
        created_at: str
            回答が作成された日時
    """

    review_request = reviews_crud.find_review_request_by_review_request_id(db, review_request_id)

    review_responses = reviews_crud.find_review_response_by_review_request_id(db, review_request_id)

    if not review_request:
        raise HTTPException(status_code=404, detail="Review request not found.")

    request = {
        "id": review_request.id,
        "curriculum_id": review_request.curriculum_id,
        "user_id": review_request.user_id,
        "title": review_request.title,
        "content": review_request.content,
        "is_closed": review_request.is_closed,
        "created_at": review_request.created_at.isoformat(),
        "updated_at": review_request.updated_at.isoformat()
    }

    li = []
    for review_response in review_responses:
        di = {
            "id": review_response.id,
            "review_request_id": review_response.id,
            "user_id": review_response.id,
            "parent_response_id": review_response.parent_response_id,
            "content": review_response.content,
            "is_read": review_response.is_read,
            "created_at": review_response.created_at.isoformat()
        }
        li.append(di)

    re_di = {
        "review_request": request,
        "responses": li
    }

    return re_di







    
