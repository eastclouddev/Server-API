import math
from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends, Request
from schemas.news import ResponsBody
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger
from cruds import news as news_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="", tags=["News"])

@router.get("/news", response_model=ResponsBody,status_code=status.HTTP_200_OK)
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