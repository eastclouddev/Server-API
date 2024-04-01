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
    
    Parameters
    ----------
    user_id: int
        取得するユーザーのID 

    Returns
    -------
    id: int 
        質問のID
    title: str
        質問のタイトル
    content: text
        質問の内容
    curriculum_id: int
        紐づいたカリキュラムのID
    created_at: datetime
        質問作成日
    is_read: bool
        未読コメントの有無
    is_closed: bool
        完了しているかどうか

    {"questions": question_list} : dict{}
        自分の質問すべての情報
    
    """

    found_question = students_crud.find_by_question(db, student_id)

    if not found_question:
        raise HTTPException(status_code=404, detail="question not found")

    return  students_crud.cereate_question_list(db, found_question)