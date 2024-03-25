from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.news import RequestBody, ResponseBody
from cruds import news as news_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/news", tags=["News"])


@router.post("", response_model=ResponseBody, status_code=status.HTTP_201_CREATED)
async def create_news(db: DbDependency, param: RequestBody):

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
	
	except Exception as e:
		logger.error(e)
		db.rollback()
		raise HTTPException(status_code=400, detail="Invalid input data.")

	return re_di