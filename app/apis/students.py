from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

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
        objective: str
            学習内容で実践したいこと
        current_situation: str
            現状
        research: str
            自分が調べたこと
        content: str
            質問の内容
        curriculum_id: int
            紐づいたカリキュラムのID
        tech_category: str
            カリキュラムのコースに紐づいた技術カテゴリ
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
        tech_category = students_crud.find_category_by_course_id(db, question.course_id)
        notifications = students_crud.find_notification_by_question_id(db, question.id)
        is_read = all([notification.is_read for notification in notifications])
        one_question = {
            "id": question.id,
            "title": question.title,
            "objective": question.objective,
            "current_situation": question.current_situation,
            "research": question.research,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "tech_category": tech_category.name,
            "created_at": question.created_at,
            "is_read": is_read,
            "is_closed": question.is_closed
        }
        
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
    reviews: dict
        id: int
            レビューのID
        title: str
            レビューのタイトル
        content: str
            レビューの内容
        curriculum_id: int
            紐づいたカリキュラムのID
        tech_category: str
            カリキュラムのコースに紐づいた技術カテゴリ
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
        tech_category = students_crud.find_category_by_curriculum_id(db, review.curriculum_id)
        notifications = students_crud.find_notification_by_review_request_id(db, review.id)
        is_read = all([notification.is_read for notification in notifications])

        di = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "tech_category": tech_category.name,
            "created_at": review.created_at.isoformat(),
            "is_read": is_read,
            "is_closed": review.is_closed
        }
        li.append(di)

    return {"reviews": li}

@router.post("/{student_id}/assign_mentor", status_code=status.HTTP_201_CREATED)
async def create_assign_mentor(db: DbDependency, student_id: int):
        
    """
    受講生と担当メンターの関連付け
    
    Parameters
    -----------------------
    student_id: int
        メンターを割り当てる受講生のID

    Returns
    -----------------------
    なし
    """

    user = students_crud.find_student_id(db, student_id)
    if not user:
        raise HTTPException(status_code=404, detail="Student ID is not found.")
    
    try:
        students_crud.find_mentor_by_least_students(db, student_id)
        db.commit()
        return
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Student ID is invalid.")