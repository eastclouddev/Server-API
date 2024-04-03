from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.students import ResponseBody
from cruds import students as students_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/{student_id}/questions", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_my_question_list(db: DbDependency, student_id: int = Path(gt=0)):

    """
    自分の質問を取得する
    
    Parameter
    -----------------------
    user_id: int
        取得するユーザーのID 

    Returns
    -----------------------
    questions: array
        id: int
            質問のID
        title: str
            質問のタイトル
        content: str
            質問の内容
        curriculum_id: int
            紐づいたカリキュラムのID
        created_at: str
            質問作成日
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
    """

    found_question = students_crud.find_by_user_id(db, student_id)

    if not found_question:
        raise HTTPException(status_code=404, detail="question not found")

    question_list = []

    for question in found_question:
        one_question = {
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "created_at": question.created_at,
            "is_closed": question.is_closed
        }
        answer = students_crud.find_by_question_id(db, question.id)
        if answer:
            find_is_read = {"is_read": answer.is_read}
            one_question.update(find_is_read)
        else:
            find_is_read = {"is_read": False}
            one_question.update(find_is_read)
        
        question_list.append(one_question)
    
    return {"questions": question_list}