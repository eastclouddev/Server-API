import math
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.news import ResponseBody,AllResponseBody,RequestBody,UpdateResponseBody
from schemas.news import DetailResponseBody, AllResponseBody, CreateRequestBody, CreateResponseBody
from cruds import news as news_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/{news_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_news_details(db: DbDependency, news_id: int = Path(gt=0)):
    """
    ニュース詳細取得

    Parameter
    -----------------------
    news_id: int
        取得するニュースのID

    Returns
    -----------------------
    dict
        id: int
            取得したニュースのID
        title: str
            ニュースのタイトル
        content: str
            ニュースの内容
        published_at: str
            ニュースの公開日（ISO 8601形式）
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
async def find_news_list(db: DbDependency, page: int, limit: int):
    """
    ニュース一覧取得

    Parameters
    -----------------------
    page: int
        表示するページ
    limit: int
        1ページに表示するニュース数

    Returns
    -----------------------
    news: array
        id: int
            ニュースのID
        title: str
            ニュースのタイトル
        published_at: str
            ニュースの公開日（ISO 8601形式）
    page: int
        表示するページ
    limit: int
        1ページに表示するニュース数
    total_page: int
        全ページ数
    total_news: int
        全ニュース数
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

@router.patch("/{news_id}", response_model= UpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_news(db: DbDependency, news_id: int, param:RequestBody):

    logger.info(param)

    found_news = news_crud.find_by_news_id(db, news_id)

    if not found_news:
        raise HTTPException(status_code=404,detail="News not found.")

    try:
        news = news_crud.update_by_news_id(db, news_id, param.title, param.content, param.is_published, param.published_at)
        db.commit()

        re_di ={
                "news_id": news.id,
                "title": news.title,
                "content": news.content,
                "is_published": news.is_published,
                "published_at": news.published_at.isoformat(),
                "updated_at": news.updated_at.isoformat()

        }

        return re_di

    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")  

@router.post("", response_model=CreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_news(db: DbDependency, param: CreateRequestBody):
    """
    ニュース作成
    Parameters
    -----------------------
    dict
        title: str
            作成するニュースのタイトル
        content: str
            作成するニュースの本文
        is_published: bool
            公開フラグ
        published_at: str
            公開日（ISO 8601形式）

    Returns
    -----------------------
    dict
        id: int
            作成されたニュースのID
        title: str
            作成されたニュースのタイトル
        content: str
            作成されたニュースの内容
        is_published: bool
            ニュースの公開フラグ
        published_at: str
            ニュースの公開日（ISO 8601形式）
        created_at: str
            ニュースの作成日（ISO 8601形式）
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