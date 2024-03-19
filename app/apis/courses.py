from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/courses", tags=["Courses"])

from cruds import courses as courses_crud
from schemas.courses import ResponseBody

@router.get("", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def get_courses(db: DbDependency):
    courses = courses_crud.find_by_courses(db)

    li = []
    for course in courses:
        di = {
            "course_id": course.id,
            "title": course.title,
            "description": course.description,
            "created_user": course.created_user,
            "thumbnail_url": course.thumbnail_url,
            "created_at": course.created_at.isoformat()
        }
        li.append(di)

    re_di = {
        "courses": li
    }

    return re_di