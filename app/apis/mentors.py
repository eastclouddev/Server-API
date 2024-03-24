from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends, Request
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger

from cruds import mentors as mentors_crud
from schemas.mentors import ResponseBody

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])

@router.get("/{mentor_id}/students/questions", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_questions(db: DbDependency, request: Request, mentor_id: int = Path(gt=0)):
	
    # TODO:ヘッダー情報をどう使うか
    header = request.headers
	
    questions = mentors_crud.find_by_questions(db, mentor_id)

    li = []
    for question in questions:
        di = {
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "created_at": question.created_at.isoformat(),
            "is_read": True, # TODO:どこから取得?
            "is_closed": question.is_closed
        }
        li.append(di)

    re_di = {
        "questions": li
    }

    return re_di