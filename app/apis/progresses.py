from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query,Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.progresses import ProgressListResponseBody
from cruds import progresses as progresses_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/progresses", tags=["Progresses"])


@router.get("", response_model=ProgressListResponseBody, status_code=status.HTTP_200_OK)
async def find_progress_list_admin(db: DbDependency):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    なし

    Returns
    -----------------------
    progresses: array
        progress_id: int
            進捗のID
        user_id: int
            ユーザーのID
        course_id: int
            コースのID
        section_id: int
            セクションのID
        curriculum_id: int
            カリキュラムのID
        progress_percentage: int
            進捗のパーセンテージ
        status: str
            ステータス
    """
    found_course_progresses = progresses_crud.find_course_progresses(db)

    progresses_list = []

    for progress in found_course_progresses:
        one_progress = {
            "progress_id": progress.id,
            "user_id": progress.user_id,
            "course_id": progress.course_id,
            "section_id": progresses_crud.find_section_by_course_id(db, progress.course_id),
            "curriculum_id": progresses_crud.find_curriculum_by_course_id(db, progress.course_id),
            "progress_percentage": progress.progress_percentage,
            "status": progresses_crud.find_status_by_status_id(db, progress.status_id)
        }

        progresses_list.append(one_progress)

    return {"progresses": progresses_list} 

