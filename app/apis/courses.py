from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.courses import AllResponseBody, DetailResponseBody
from cruds import courses as courses_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", response_model=AllResponseBody, status_code=status.HTTP_200_OK)
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

@router.get("/{course_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_course(db: DbDependency, course_id: int = Path(gt=0)):
    course = courses_crud.find_by_course(db, course_id)
    sections = courses_crud.find_by_sections(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    section_li = []
    if sections:
        for section in sections:
            curriculums = courses_crud.find_by_curriculums(db, section.id)
            curriculum_li = []
            # 最内のリストを作成
            for curriculum in curriculums:
                curriculum_di = {
                    "curriculum_id": curriculum.id,
                    "title": curriculum.title,
                    "description": curriculum.description
                }
                curriculum_li.append(curriculum_di)

            section_di = {
                "section_id": section.id,
                "title": section.title,
                "description": section.description,
                "curriculums": curriculum_li
            }
            section_li.append(section_di)
    
    re_di = {
        "course_id": course.id,
        "title": course.title,
        "description": course.description,
        "created_user_id": course.created_user,
        "created_at": course.created_at.isoformat(),
        "sections": section_li
    }
	
    return re_di