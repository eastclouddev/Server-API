from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.reviews import ReviewResponseUpdateRequestBody, ReviewResponseUpdateResponseBody, \
                            ReviewRequestUpdateRequestBody, ReviewRequestUpdateResponseBody, \
                            ReviewThreadDetailResponseBody, ReviewResponseCreateResponseBody, ReviewResponseCreateRequestBody

from cruds import reviews as reviews_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/{review_request_id}/responses", response_model=ReviewResponseCreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_review_resposne(db: DbDependency, param: ReviewResponseCreateRequestBody, review_request_id: int):
    """
    レビュー回答作成

    Parameters
    -----------------------
    dict
        user_id: int
            回答を投稿するユーザーのID
        parent_response_id: int
            返信先の回答ID
        content: str
            回答の内容
        media_content: json
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
    review_request_id: int
        回答を投稿したいレビューリクエストのID

    Returns
    -----------------------
    dict
        id: int
            新しく作成された回答のID
        review_request_id: int
            回答が紐づくレビューリクエストのID
        user: dict
            user_id: int
                回答を投稿したユーザーのID
            name: str
                回答を投稿したユーザーの名前
        parent_response_id: int
            返信先の回答ID
        content: str
            回答の内容
        media_content: json
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
        created_at: str
            回答が作成された日時（ISO8601形式）
    """

    new_review_response = reviews_crud.create_review_response(db, param, review_request_id)

    if not new_review_response:
        raise HTTPException(status_code=404, detail="Review request not found.")
    
    try:
        db.commit()

        user = reviews_crud.find_user_by_id(db, param.user_id)

        re_di = {
            "id": new_review_response.id,
            "review_request_id": new_review_response.review_request_id,
            "user": {
                "user_id": param.user_id,
                "name": user.last_name + user.first_name
            },
            "parent_response_id": new_review_response.parent_response_id,
            "content": new_review_response.content,
            "media_content": new_review_response.media_content,
            "created_at": new_review_response.created_at.isoformat()
        }

        return re_di

    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.patch("/responses/{response_id}", response_model=ReviewResponseUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_review_response(db: DbDependency, update: ReviewResponseUpdateRequestBody, response_id: int = Path(gt=0)):
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
    
    new_response = reviews_crud.update_response(db, update, response_id)
    if not new_response:
        raise HTTPException(status_code=404, detail="Response not found.")

    try:
        db.commit()
        return new_response

    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")


@router.patch("/{review_id}", response_model=ReviewRequestUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_review_request(db: DbDependency, update: ReviewRequestUpdateRequestBody, review_id: int = Path(gt=0)):
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
    
    new_review = reviews_crud.update_review(db, update, review_id)
    if not new_review:
        raise HTTPException(status_code=404, detail="Curriculum not found.")

    try:
        db.commit()
        return new_review

    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
 

@router.get("/{review_request_id}", response_model=ReviewThreadDetailResponseBody, status_code=status.HTTP_200_OK)
async def find_review_thread_details(db: DbDependency, review_request_id: int):
    """
    レビュースレッド詳細
    
    Parameter
    -----------------------
    review_request_id: int
        スレッド詳細を取得したいレビューリクエストのID

    Returns
    -----------------------
    review_request: dict
        id: int
            レビューリクエストのID
        curriculum_id: int
            関連するカリキュラムのID
        user: dict
            user_id: int
                レビューリクエストを投稿したユーザーのID
            name: str
                レビューリクエストを投稿したユーザーの名前
        title: str
            レビューリクエストのタイトル
        content: str
            レビューリクエストの内容
        media_content: json
            レビューに関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
        is_closed: bool
            レビューリクエストがクローズされているかどうか
        created_at: str
            レビューリクエストが作成された日時（ISO8601形式）
    review_responses: array
        id: int
            回答のID
        review_request_id: int
            回答が紐づくレビューリクエストのID
        user: dict
            user_id: int
                回答を投稿したユーザーのID
            name: str
                回答を投稿したユーザーの名前
        parent_response_id: int
            返信先の回答ID
        content: str
            回答の内容
        media_content: json
            回答に関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
        created_at: str
            回答が作成された日時（ISO8601形式）
    """

    review_request = reviews_crud.find_review_request_by_review_request_id(db, review_request_id)

    review_responses = reviews_crud.find_review_response_by_review_request_id(db, review_request_id)

    if not review_request:
        raise HTTPException(status_code=404, detail="Review request not found.")
    
    user = reviews_crud.find_user_by_id(db, review_request.user_id)

    request = {
        "id": review_request.id,
        "curriculum_id": review_request.curriculum_id,
        "user": {
            "user_id": review_request.user_id,
            "name": user.last_name + user.first_name
        },
        "title": review_request.title,
        "content": review_request.content,
        "media_content": review_request.media_content,
        "is_closed": review_request.is_closed,
        "created_at": review_request.created_at.isoformat()
    }

    li = []
    for review_response in review_responses:
        user = reviews_crud.find_user_by_id(db, review_response.user_id)
        di = {
            "id": review_response.id,
            "review_request_id": review_response.review_request_id,
            "user": {
                "user_id": review_response.user_id,
                "name": user.first_name + user.last_name
            },
            "parent_response_id": review_response.parent_response_id,
            "content": review_response.content,
            "media_content": review_response.media_content,
            "created_at": review_response.created_at.isoformat()
        }
        li.append(di)

    re_di = {
        "review_request": request,
        "review_responses": li
    }

    return re_di







    
