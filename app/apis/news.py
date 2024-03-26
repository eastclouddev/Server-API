import math
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.news import ResponseBody, AllResponseBody
from cruds import news as news_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/{news_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_by_news_id(db: DbDependency, news_id: int = Path(gt=0)):

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

    news = news_crud.find_by_news(db)

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