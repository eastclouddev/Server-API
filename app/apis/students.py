from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.students import ResponseBody, AllResponseBody, ProgressesResponse, NotificationListResponseBody
from schemas.students import QuestionListResponseBody, ReviewRequestListResponseBody, ProgressListResponseBody
from cruds import students as students_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/{student_id}/questions", response_model=QuestionListResponseBody, status_code=status.HTTP_200_OK)
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

    found_question = students_crud.find_questions_by_user_id(db, student_id)

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
        answer = students_crud.find_answer_by_question_id(db, question.id)
        if answer:
            find_is_read = {"is_read": answer.is_read}
            one_question.update(find_is_read)
        else:
            find_is_read = {"is_read": False}
            one_question.update(find_is_read)
        
        question_list.append(one_question)
    
    return {"questions": question_list}

@router.get("/{student_id}/progresses", response_model=ProgressListResponseBody, status_code=status.HTTP_200_OK)
async def find_progress_list_student(db: DbDependency, reqeust: Request):
    """
    現在の学習進捗
    Parameters
    -----------------------
    request: Request
        headersから情報を取得する

    Returns
    -----------------------
    progresses: array
        course_id: int
            コースのID
        course_title: str
            コースのタイトル
        progress_percentage: int
            コースの進捗率
        status: str
            コースのステータス
        last_accessed_at: str
            最終アクセス日（ISO 8601形式）
    """
    # TODO:ヘッダー情報から必要なパラメータを取得する
    user_id = 1

    progresses = students_crud.find_course_progresses_by_user_id(db, user_id)
                
    li = []

    for progress in progresses:
        course = students_crud.find_course_by_course_id(db, progress.course_id)
        status = students_crud.find_status_by_status_id(db, progress.status_id)

        if course and status:
            di = {
                "course_id": progress.course_id,
                "course_title": course.title,
                "progress_percentage": progress.progress_percentage,
                "status": status.name,
                "last_accessed_at": progress.last_accessed_at.isoformat()
            }
            li.append(di)

    re_di = {
        "progresses": li
    }

    return re_di
  
@router.get("/{student_id}/reviews", response_model=ReviewRequestListResponseBody, status_code=status.HTTP_200_OK)
async def find_my_review_list(db: DbDependency, student_id: int):

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

    review_requests = students_crud.find_review_requests_by_user_id(db, student_id)

    li = []
    for review in review_requests:
        review_responses = students_crud.find_review_responses_by_review_id(db, review.id)
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

@router.get("/{student_id}/notifications", response_model=NotificationListResponseBody, status_code=status.HTTP_200_OK)
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
    related_review_response_id: int
        レビューレスポンスのID
    is_read: bool
        通知が既読かどうか
    created_at: str
        作成日時

    """
    mentors = students_crud.find_mentor_by_student_id(db, student_id)

    if not mentors:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2つのテーブルから取得
    li = []
    user_id_list = [mentor.mentor_id for mentor in mentors]
    two_tables = students_crud.find_table(db, user_id_list)
    for data in two_tables:
        di = {
            "id": data[0],
            "content": data[1],
            "created_at": data[2]
        }
        li.append(di)

    # 作成日が新しい順に並び替える
    re_sorted = sorted(li, key=lambda x:x["created_at"], reverse=True)
    # 並び替えたものから先頭10件取得
    re_sorted = re_sorted[:10]
    count = 1
    li = []

    for r in re_sorted:
        table, data = students_crud.find_db(db, r["id"], r["content"], r["created_at"])
        mentor = students_crud.find_user_by_user_id(db, data.user_id)

        di = {
            "id": count,
            "from_user_id": mentor.id,
            "from_user_name": mentor.last_name + mentor.first_name,
            "content": data.content,
            "related_question_id": data.question_id if table == "answer" else None,
            "related_answer_id": data.id if table == "answer" else None,
            "related_review_request_id": data.review_request_id if table == "response" else None,
            "related_review_response_id": data.id if table == "response" else None,
            "is_read": data.is_read,
            "created_at": data.created_at.isoformat()
        }
        li.append(di)

        count += 1

    return {"notifications": li}