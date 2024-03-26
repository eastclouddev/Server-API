from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from logging import getLogger
from typing import Annotated
from database.database import get_db
from schemas.questions import  ResponseBody
from cruds import questions as questions_crud
from services import questions as questions_service

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/questions", tags=["QuestionsThreadList"])


@router.get("/{question_id}",response_model=ResponseBody, status_code=status.HTTP_200_OK)
def get_questions_thread(db: DbDependency,question_id: int):

    """
    質問スレッド一覧取得
    
    Parameters
    ----------
    なし

    Returns
    -------
    {
        {"question":}
        {"answers": answers_list}
    }
            : dic{}
            質問スレッド一覧
    
    """

    found_question = questions_crud.find_question(db,question_id)
    found_answers = questions_crud.find_answers(db,question_id)

    
    answer_list = questions_service.create_answers_list(found_answers)
    
    return {"question":found_question,"answer":answer_list}