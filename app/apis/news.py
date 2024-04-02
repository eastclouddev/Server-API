import math
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.news import DetailResponseBody, AllResponseBody, CreateRequestBody, CreateResponseBody
from cruds import news as news_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/{news_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_by_news_id(db: DbDependency, news_id: int = Path(gt=0)):
    """
    ニュース詳細取得
    Parameters
    ----------
    news_id: int
        取得するニュースのID

    Returns
    -------
    re_di: DetailResponseBody
        id, title, content, published_at
    """

    news = news_crud.find_by_news_id(db, news_id)

    if not news:
        raise HTTPException(status_code=404, detail="The requested news article was not found.")

    re_di = {
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "published_at": news.published_at.isoformat()
    }

    return re_di

@router.get("", response_model=AllResponseBody, status_code=status.HTTP_200_OK)
async def get_receipt(db: DbDependency, page: int, limit: int):
    """
    ニュース一覧取得
    Parameters
    ----------
    page: int
        表示するページ
    limit: int
        1ページに表示するニュース数

    Returns
    -------
    re_di: AllResponseBody
        news[], page, limit, total_page, total_news
    """
    news = news_crud.find_news(db)

    li = []
    
    for data in news[(page-1)*limit : page*limit]:
        di = {
            "id": data.id,
            "title": data.title,
            "published_at": data.published_at.isoformat()
        }
        li.append(di)

    re_di = {
        "news": li,
        "page": page,
        "limit": limit,
        "total_pages": math.ceil(len(news) / limit),
        "total_news": len(news)
    }

    return re_di

@router.post("", response_model=CreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_news(db: DbDependency, param: CreateRequestBody):
    """
    ニュース作成
    Parameters
    ----------
    param: CreateRequestBody
        title, content, is_published, published_at        

    Returns
    -------
    re_di: CreateResponseBody
        id, title, content, is_published, published_at, created_at
    """

    try:

        new_news = news_crud.create_news(db, param)
        db.commit()

        re_di = {
            "id": new_news.id,
            "title": new_news.title,
            "content": new_news.content,
            "is_published": new_news.is_published,
            "published_at": new_news.published_at.isoformat(),
            "created_at": new_news.created_at.isoformat()
        }

        return re_di
	
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")