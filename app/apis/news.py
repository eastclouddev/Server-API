from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/news", tags=["News"])

from schemas.news import ResponseBody
from cruds import news as news_crud

@router.get("/{news_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_by_news_id(db: DbDependency, news_id: int = Path(gt=0)):

    news = news_crud.find_by_news_id(db, news_id)

    if not news:
        raise HTTPException(status_code=404, detail="The requested news article was not found.")

    re_di = {
      "id": news.id,
      "title": news.title,
      "summary": news.summary,
      "content": news.content,
      "published_at": news.published_at.isoformat()
    }

    return re_di