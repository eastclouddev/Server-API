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
    -----------------------
    dict
        user_id: int
            回答するユーザーのID
        content: str
            回答

    Returns
    -----------------------
    dict
        answer_id: int
            作成された回答のID
        question_id: int
            回答に紐づく質問のID
        user_id: int
            回答したユーザーのID
        content: str
            回答
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
    
    Parameter
    -----------------------
    なし

    Returns
    -----------------------
    dict
        question: dict
            id: int
                質問のID
            curriculum_id: int
                質問が含まれるカリキュラムのID
            user_id: int
                質問を投稿したユーザーのID
            title: int
                質問のタイトル
            content: str
                質問の内容
            media_content: json
                質問に関するメディアコンテンツの情報
            is_closed: bool
                質問がクローズされているか
            created_at: str
                作成日（ISO 8601形式）
        answer: array
            id: int
                回答のID
            question_id: int
                回答が紐づく質問のID
            user_id: int
                回答を投稿したユーザーのID
            parent_answer_id: int or None
                返信先の回答ID（返信先がない場合はNoneが返る）
            content: str
                回答の内容
            media_content: json
                回答に関するメディアコンテンツの情報
            is_read: bool
                回答が既読かどうかを示すフラグ
            created_at: str
                作成日（ISO 8601形式）
    """

    found_question = questions_crud.find_question(db, question_id)

    if not found_question:
        raise HTTPException(status_code=404,detail="Question not found.")
    
    question = {
        "id":found_question.id,
        "curriculum_id":found_question.curriculum_id,
        "user_id":found_question.user_id,
        "title":found_question.title,
        "content":found_question.content,
        "media_content":found_question.media_content,
        "is_closed":found_question.is_closed,
        "created_at":found_question.created_at.isoformat()
    }

    found_answers = questions_crud.find_answers(db, question_id)
    answer_list = []
    for answer in found_answers:
        one_answer = {
            "id": answer.id,
            "question_id": answer.question_id,
            "user_id": answer.user_id,
            "parent_answer_id": answer.parent_answer_id,
            "content": answer.content,
            "media_content": answer.media_content,
            "is_read": answer.is_read,
            "created_at": answer.created_at.isoformat()
        }

        answer_list.append(one_answer)
    
    re_di = {
        "question": question,
        "answer": answer_list
    }
    
    return re_di