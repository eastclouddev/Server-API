from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends, Request
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger
from schemas.state_progresses import ResponseBody
from models.course_progresses import CourseProgresses
from models.courses import Courses
from models.learning_statuses import LearningStatuses
from cruds import state_progresses as state_progresses_crud


logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="", tags=["StateProgresses"])

#@router.get("/state_progresses", status_code=status.HTTP_200_OK)
@router.get("/state_progresses",response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def get_receipt(db: DbDependency, reqeust: Request):

    # TODO:ヘッダー情報から必要なパラメータを取得する
    user_id = 1

    progresses = state_progresses_crud.find_by_course_progresses(db, user_id)
    #progresses = db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id).all()
                
    li = []

    for progress in progresses:
        course = state_progresses_crud.find_by_course(db,progress.course_id)
        status = state_progresses_crud.find_by_status(db,progress.status_id)

        # course = db.query(Courses).filter(Courses.id == progress.course_id).first()
        # status = db.query(LearningStatuses).filter(LearningStatuses.id == progress.status_id).first()
        if course and status:
            di = {
                "course_id": progress.course_id,
                "course_title": course.title,
                "progress_percentage": progress.progress_percentage,
                "status": status.name,
                "last_accessed_at": progress.last_accessed_at.isoformat()
            }
            li.append(di)


    re_di = {
        "progresses": li
    }

    return re_di