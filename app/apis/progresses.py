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
async def find_progress_list_admin(db: DbDependency, name: str = "", company: str = ""):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    検索
        name: str
        company: str

    Returns
    -----------------------
    progresses: array
        user_id: int
            ユーザーのID
        user_name: str
            ユーザーの名前
        course_id: int
            コースのID
        course_name: str
            コースの名前
        section_id: int
            セクションのID
        curriculum_id: int
            カリキュラムのID
        progress_percentage: int
            進捗のパーセンテージ
        status: str
            ステータス
    """
    course_progresses = progresses_crud.find_course_progresses(db)
    companies = progresses_crud.find_companies_by_name(db, company)
    company_id_list = [com.id for com in companies]

    li = []
    for progress in course_progresses:
        user = progresses_crud.find_user_by_id(db, progress.user_id)
        if any([
            name and (name in user.first_name),
            name and (name in user.last_name),
            name and (name in user.first_name_kana),
            name and (name in user.last_name_kana),
            name and (name in (user.last_name + user.first_name)),
            name and (name in (user.last_name_kana + user.first_name_kana)),
            company and (user.company_id in company_id_list),
            name == "" and company == ""
        ]):
            course = progresses_crud.find_course_by_course_id(db, progress.course_id)
            di = {
                "user_id": progress.user_id,
                "user_name": user.last_name + user.first_name,
                "course_id": progress.course_id,
                "course_name": course.title,
                "section_id": progresses_crud.find_section_by_course_id(db, progress.course_id),
                "curriculum_id": progresses_crud.find_curriculum_by_course_id(db, progress.course_id),
                "progress_percentage": progress.progress_percentage,
                "status": progresses_crud.find_status_by_status_id(db, progress.status_id)
            }
            li.append(di)

    return {"progresses": li} 

