from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.curriculums import ReviewsResponseBody, DetailResponseBody, ReviewResponse, ReviewRequestBody
from cruds import curriculums as curriculums_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/curriculums", tags=["Curriculums"])

@router.get("/{curriculum_id}/reviews", response_model=ReviewsResponseBody, status_code=status.HTTP_200_OK)
async def find_review_list(db: DbDependency, curriculum_id: int = Path(gt=0)):
    """
    カリキュラムのレビュー一覧

    Parameter
    -----------------------
    curriculum_id: int
        レビュー一覧を取得したいカリキュラムのID

    Returns
    -----------------------
    reviews: array
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
            レビューリクエストが作成された日時（ISO 8601形式）
        updated_at: str
            レビューリクエストが最後に更新された日時（ISO 8601形式）
    """

    reviews = curriculums_crud.find_reviews(db, curriculum_id)

    li = []
    for review in reviews:
        di = {
            "id": review.id,
            "curriculum_id": review.curriculum_id,
            "user_id": review.user_id,
            "title": review.title,
            "content": review.content,
            "is_closed": review.is_closed,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        }
        li.append(di)

    re_di = {
        "reviews": li
    }

    return re_di

@router.get("/{curriculum_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_curriculum_details(db: DbDependency, curriculum_id: int = Path(gt=0)):
    """
    カリキュラム詳細取得

    Parameter
    -----------------------
    curriculum_id: int
        詳細を取得したいカリキュラムのID

    Returns
    -----------------------
    dict
        curriculum_id: int
            カリキュラムのID
        title: str
            カリキュラムのタイトル
        description: str
            カリキュラムの詳細な説明
        video_url: str
            ビデオコンテンツのURL(ビデオが存在する場合のみ）
        content: str 
            カリキュラムのテキストコンテンツ(テキストコンテンツが存在する場合のみ）
        is_test: boolean
            このカリキュラムがテストかどうかを示すフラグ（boolean）
        display_no: int
            カリキュラムの表示順
    """
    info = curriculums_crud.find_by_curriculum_id(db, curriculum_id)
    if not info:
        raise HTTPException(status_code=404, detail="Curriculum not found.")
    return info

@router.post("/{curriculum_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_curriculum_id(db: DbDependency, param: ReviewRequestBody, curriculum_id: int):

    found_curriculum = curriculums_crud.find_by_reviews(db,curriculum_id)

    if not found_curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found.")

    try:
        reviews = curriculums_crud.create_reviews(db, curriculum_id, param.user_id, param.title, param.content, param.is_closed)
        db.commit()

    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.") 

    di = {
            "id": reviews.id,
            "curriculum_id": reviews.curriculum_id,
            "user_id": reviews.user_id,
            "title": reviews.title,
            "content": reviews.content,
            "is_closed": reviews.is_closed,
            "created_at": reviews.created_at.isoformat()
            }
    
    return di