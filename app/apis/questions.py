from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.questions import AnswerCreateRequestBody, AnswerCreateResponseBody, QuestionThreadDetailResponseBody, \
                                AnswerUpdateRequestBody, AnswerUpdateResponseBody, \
                                QuestionUpdateRequestBody, QuestionUpdateResponseBody
from cruds import questions as questions_crud
from services import questions as questions_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/{question_id}/answers", response_model=AnswerCreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_answer(db: DbDependency, param: AnswerCreateRequestBody, question_id: int):
    """
    質問回答投稿作成

    Parameters
    -----------------------
    dict
        user_id: int
            回答するユーザーのID
        parent_answer_id: int
            返信先の回答ID
        content: str
            回答
        media_content: json
            関連するメディアコンテンツの情報

    Returns
    -----------------------
    dict
        answer_id: int
            作成された回答のID
        question_id: int
            回答に紐づく質問のID
        parent_answer_id: int
            返信先の回答ID
        user: dict
            user_id: int
                回答したユーザーのID
            name: str
                回答したユーザーの名前
        content: str
            回答
        media_content: json
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
        created_at: str
            回答が作成された日時（ISO8601形式）
    """

    question = questions_crud.find_question_by_question_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    
    try:
        # answer = questions_crud.find_answer_by_question_id(db, question_id)

        # # 同じ質問に対して、再度回答する場合はparent_answer_idを追加する
        # if answer:
        #     new_answer = questions_crud.create_answer_parent_answer_id(db, param, question_id, answer.id)
        # else:
        #     new_answer = questions_crud.create_answer(db, param, question_id)
        new_answer = questions_crud.create_answer(db, param, question_id)
        db.commit()

        user = questions_crud.find_user_by_id(db, param.user_id)

        re_di = {
            "answer_id": new_answer.id,
            "question_id": new_answer.question_id,
            "parent_answer_id": param.parent_answer_id,
            "user": {
                "user_id": new_answer.user_id,
                "name": user.last_name + user.first_name,
            },
            "content": new_answer.content,
            "media_content": new_answer.media_content,
            "created_at": new_answer.created_at.isoformat()
        }

        return re_di
    
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{question_id}", response_model=QuestionThreadDetailResponseBody, status_code=status.HTTP_200_OK)
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
            user: dict
                user_id: int
                    質問を投稿したユーザーのID
                name: str
                    質問を投稿したユーザーの名前
            title: int
                質問のタイトル
            objective: str
                学習内容で実践したこと
            current_situation: str
                現状
            research: str
                自分で調べたこと
            content: str
                質問の内容
            media_content: json
                質問に関するメディアコンテンツの情報
                url: str
                    メディアコンテンツのURL
            is_closed: bool
                質問がクローズされているか
            created_at: str
                作成日（ISO 8601形式）
        answer: array
            id: int
                回答のID
            question_id: int
                回答が紐づく質問のID
            user: dict
                user_id: int
                    回答を投稿したユーザーのID
                name: str
                    回答を投稿したユーザーの名前                
            parent_answer_id: int or None
                返信先の回答ID（返信先がない場合はNoneが返る）
            content: str
                回答の内容
            media_content: json
                回答に関するメディアコンテンツの情報
                url: str
                    メディアコンテンツのURL
            created_at: str
                作成日（ISO 8601形式）
    """

    found_question = questions_crud.find_question_by_question_id(db, question_id)

    if not found_question:
        raise HTTPException(status_code=404,detail="Question not found.")
    
    user = questions_crud.find_user_by_id(db, found_question.user_id)
    media_content = []
    for content in found_question.media_content:
        if content.get("url"):
            media_content.append({"url": content.get("url")})
    
    question = {
        "id": found_question.id,
        "curriculum_id": found_question.curriculum_id,
        "user": {
            "user_id": user.id,
            "name": user.last_name + user.first_name
        },
        "title": found_question.title,
        "objective": found_question.objective,
        "current_situation": found_question.current_situation,
        "research": found_question.research,
        "content": found_question.content,
        "media_content": media_content,
        "is_closed": found_question.is_closed,
        "created_at": found_question.created_at.isoformat()
    }

    found_answers = questions_crud.find_answers_by_question_id(db, question_id)
    answer_list = []
    for answer in found_answers:
        user = questions_crud.find_user_by_id(db, answer.user_id)
        one_answer = {
            "id": answer.id,
            "question_id": answer.question_id,
            "user": {
                "user_id": user.id,
                "name": user.last_name + user.first_name
            },
            "parent_answer_id": answer.parent_answer_id,
            "content": answer.content,
            "media_content": answer.media_content,
            "created_at": answer.created_at.isoformat()
        }

        answer_list.append(one_answer)
    
    re_di = {
        "question": question,
        "answer": answer_list
    }
    
    return re_di

@router.patch("/{question_id}", response_model=QuestionUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_question(db: DbDependency, param: QuestionUpdateRequestBody, question_id: int):
    """
    質問編集

    Parameter
    -----------------------
    question_id: int
        更新したい質問のID
    title: str
        更新された質問のタイトル
    content: str
        更新したい質問の内容
    media_content: json
        更新したい質問に関連するメディアコンテンツの情報
    is_closed: bool
        完了しているかどうかを表すフラグ
    
    Returns
    -----------------------
    dict
        id: int
            更新された質問のID
        curriculum_id: int
            回答が紐づくカリキュラムのID
        user_id: int
            回答を投稿したユーザーのID
        title: str
            更新された質問のタイトル
        content: str
            更新された質問の内容
        media_content: Optional[json]
            更新されたメディアコンテンツの情報
        is_closed: bool
            質問が完了しているかどうかを示すフラグ（boolean）
        updated_at: str
            質問が最後に更新された日時（ISO 8601形式）
    """

    question = questions_crud.update_question(db, param, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")
    
    try:
        db.commit()
        info = {
            "id": question.id,
            "curriculum_id": question.curriculum_id,
            "user_id": question.user_id,
            "title": question.title,
            "content": question.content,
            "media_content": question.media_content,
            "is_closed": question.is_closed,
            "updated_at": question.updated_at.isoformat()
        }

        return info

    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.patch("/answers/{answer_id}", response_model=AnswerUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_answer(db: DbDependency, param: AnswerUpdateRequestBody, answer_id: int):
    """
    質問回答更新（受講生、メンター）

    Parameter
    -----------------------
    answer_id: int
        更新したい回答のID
    content: str
        更新したい回答の内容
    media_content: json
        更新したい回答に関連するメディアコンテンツの情報
    is_read: bool
        回答か既読かを表すフラグ

    Returns
    -----------------------
    dict
        id: int
            更新された回答のID
        question_id: int
            回答が紐づく質問のID
        user_id: int
            回答を投稿したユーザーのID
        parent_answer_id: Optional[int]
            返信先の回答ID
        content: str
            更新された回答の内容
        media_content: Optional[json]
            更新されたメディアコンテンツの情報
        is_read: bool
            回答が既読かどうかを示すフラグ（boolean）
        updated_at: str
            回答が最後に更新された日時（ISO 8601形式）
    """

    answer = questions_crud.update_answer(db, param, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found.")
    
    try:
        db.commit()
        re_di = {
            "id": answer.id,
            "question_id": answer.question_id,
            "user_id": answer.user_id,
            "parent_answer_id": answer.parent_answer_id,
            "content": answer.content,
            "media_content": answer.media_content,
            "is_read": answer.is_read,
            "updated_at": answer.updated_at.isoformat()
        }

        return re_di
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")