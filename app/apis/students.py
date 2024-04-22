from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.students import ResponseBody, AllResponseBody, ListResponseBody
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

@router.get("/{student_id}/reviews", response_model=AllResponseBody, status_code=status.HTTP_200_OK)
async def find_review(db: DbDependency, student_id: int):

    """
    自分のレビュー一覧取得
    
    Parameters
    -----------------------
    user_id:int
        ユーザーのID

    Returns
    -----------------------
    id: int
        レビューのID
    title: str
        レビューのタイトル
    content: str
        レビューの内容
    curriculum_id: int
        紐づいたカリキュラムのID
    created_at: str
        レビュー作成日
    is_read: bool
        未読コメントの有無
    is_closed: bool
        完了しているかどうか

    """

    reviews = students_crud.find_reviews(db, student_id)

    li = []
    for review in reviews:
        review_responses = students_crud.find_is_read(db,review.id)
        is_read = True
        for review_response in review_responses:
            data = review_response.is_read
            if data == False:
                is_read = False

        di = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "created_at": review.created_at.isoformat(),
            "is_read": is_read,
            "is_closed": review.is_closed
        }
        li.append(di)

    return {"reviews": li}

@router.get("/{student_id}/notifications", response_model=ListResponseBody, status_code=status.HTTP_200_OK)
async def find_notification(db: DbDependency, student_id: int):

    """
    通知一覧(受講生)
    
    Parameters
    -----------------------
    student_id:int
        ユーザーのID

    Returns
    -----------------------
    id: int
        通知のID
    from_user_id: int
        ユーザーのID
    from_user_name: str
        ユーザーの名前
    content: str
        通知の内容
    related_question_id: int
        質問のID
    related_answer_id: int
        回答のID
    related_review_request_id: int
        レビューリクエストのID
    related_review_respomse_id: int
        レビューリスポンスのID
    is_read: bool
        通知が既読かどうか
    created_at: str

    """

    user = students_crud.find_user_by_student_id(db,student_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    questions = students_crud.find_by_user_id(db,student_id)

    review_requests = students_crud.find_reviews(db,student_id)

    li = []
    count = 1
    for question in questions:
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.first_name + user.last_name,
            "content": question.content,
            "related_question_id": question.id,
            "related_answer_id": None,
            "related_review_request_id": None,
            "related_review_response_id": None,
            "is_read": True,#TODO:db追加
            "created_at": question.created_at.isoformat()
        }
        li.append(di)
        count = count + 1
        answers = students_crud.find_answers_by_question_id(db,question.id)
        for answer in answers:
            di = {
                "id": count,
                "from_user_id": user.id,
                "from_user_name": user.first_name + user.last_name,
                "content": answer.content,
                "related_question_id": question.id,
                "related_answer_id": answer.id,
                "related_review_request_id": None,
                "related_review_response_id": None,
                "is_read": answer.is_read,
                "created_at": answer.created_at.isoformat()
            }
            li.append(di)
            count = count +1
    
    for review_request in review_requests:
        di = {
            "id": count,
            "from_user_id": user.id,
            "from_user_name": user.first_name + user.last_name,
            "content": review_request.content,
            "related_question_id": None,
            "related_answer_id": None,
            "related_review_request_id": review_request.id,
            "related_review_response_id": None,
            "is_read": True,#TODO:db追加
            "created_at": review_request.created_at.isoformat()
        }
        li.append(di)
        count = count + 1
        review_responses = students_crud.find_is_read(db,review_request.id)
        for  review_response in review_responses:
            di = {
                "id": count,
                "from_user_id": user.id,
                "from_user_name": user.first_name + user.last_name,
                "content": review_response.content,
                "related_question_id": None,
                "related_answer_id": None,
                "related_review_request_id": review_request.id,
                "related_review_response_id": review_response.id,
                "is_read": review_response.is_read,
                "created_at": review_response.created_at.isoformat()
            }
            li.append(di)
            count = count +1

    return {"notifications": li}