from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.questions import CreateRequestBody, CreateResponseBody, DetailResponseBody
from cruds import questions as questions_crud
from services import questions as questions_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/{question_id}/answers", response_model=CreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_question_answer(db: DbDependency, param: CreateRequestBody, question_id: int = Path(gt=0)):
    """
    質問回答投稿作成
    Parameters
    ----------
    param: CreateRequestBody
        user_id, content

    Returns
    -------
    re_di: CreateResponseBody
        answer_id, question_id, user_id, content
    """

    question = questions_crud.find_by_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    
    try:
        answer = questions_crud.find_by_answer(db, question_id)

        # 同じ質問に対して、再度回答する場合はparent_answer_idを追加する
        if answer:
            new_answer = questions_crud.create_answer_parent_answer_id(db, param, question_id, answer.id)
        else:
            new_answer = questions_crud.create_answer(db, param, question_id)
        db.commit()

        re_di = {
            "answer_id": new_answer.id,
            "question_id": new_answer.question_id,
            "user_id": new_answer.user_id,
            "content": new_answer.content
        }

        return re_di
    
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{question_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_question_thread_details(db: DbDependency, question_id: int):
    """
    質問スレッド詳細取得
    
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
    
    re_di = {
        "question": found_question,
        "answer": answer_list
    }
    
    return re_di