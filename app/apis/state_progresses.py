from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.state_progresses import ResponseBody
from cruds import state_progresses as state_progresses_crud


logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/state_progresses", tags=["StateProgresses"])

@router.get("",response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def get_receipt(db: DbDependency, reqeust: Request):

    # TODO:ヘッダー情報から必要なパラメータを取得する
    user_id = 1

    progresses = state_progresses_crud.find_by_course_progresses(db, user_id)
                
    li = []

    for progress in progresses:
        course = state_progresses_crud.find_by_course(db, progress.course_id)
        status = state_progresses_crud.find_by_status(db, progress.status_id)

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