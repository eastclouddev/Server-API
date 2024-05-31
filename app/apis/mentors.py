from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.mentors import QuestionListResponseBody, ProgressListResponseBody, ReviewRequestListResponseBody, MentorsCountListResponseBody
from cruds import mentors as mentors_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])


@router.get("/{mentor_id}/progresses", response_model=ProgressListResponseBody, status_code=status.HTTP_200_OK)
async def find_progress_list_mentor(db: DbDependency, mentor_id: int):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    なし

    Returns
    -----------------------
    progresses: array
        progress_id: int
            進捗のID
        user_id: int
            ユーザーのID
        course_id: int
            コースのID
        section_id: int
            セクションのID
        curriculum_id: int
            カリキュラムのID
        progress_percentage: int
            進捗のパーセンテージ
        status: str
            ステータス
    """
    found_course_progresses = mentors_crud.find_course_progresses(db, mentor_id)
    if not found_course_progresses:
        raise HTTPException(status_code=404, detail="progresses not found")

    progresses_list = []
    for progress in found_course_progresses:
        one_progress = {
            "progress_id": progress.id,
            "user_id": progress.user_id,
            "course_id": progress.course_id,
            "section_id": mentors_crud.find_section_by_course_id(db, progress.course_id),
            "curriculum_id": mentors_crud.find_curriculum_by_course_id(db, progress.course_id),
            "progress_percentage": progress.progress_percentage,
            "status": mentors_crud.find_status_by_status_id(db, progress.status_id)
        }
        progresses_list.append(one_progress)

    return {"progresses": progresses_list} 

@router.get("/{mentor_id}/students/questions", response_model=QuestionListResponseBody, status_code=status.HTTP_200_OK)
async def find_question_list_from_student(db: DbDependency, request: Request, mentor_id: int = Path(gt=0)):
    """
    受講生からの質問一覧取得

    Parameter
    -----------------------
    mentor_id: int
        質問を取得するメンターのユーザーID

    Returns
    -----------------------
    questions: array
        id: int
            新しく作成された送金先情報のID
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
        curriculum_id: str
            質問が紐づくカリキュラムのID
        tech_category: str
            カリキュラムのコースに紐づいた技術カテゴリ
        created_at: str
            質問作成日
        is_read: str
            未読コメントの有無
        is_closed: str
            完了しているかどうか
    """
	
    questions = mentors_crud.find_questions_by_mentor_id(db, mentor_id)

    li = []
    for question in questions:
        # questionからcourseを取得し、courseに紐づくtech_categoryを取得
        tech_category = mentors_crud.find_category_by_course_id(db, question.course_id)
        notifications = mentors_crud.find_notification_by_question_id(db, question.id)
        is_read = all([notification.is_read for notification in notifications])

        di = {
            "id": question.id,
            "title": question.title,
            "objective": question.objective,
            "current_situation": question.current_situation,
            "research": question.research,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "tech_category": tech_category.name,
            "created_at": question.created_at.isoformat(),
            "is_read": is_read,
            "is_closed": question.is_closed
        }
        li.append(di)

    re_di = {
        "questions": li
    }

    return re_di 



@router.get("/{mentor_id}/students/reviews", response_model=ReviewRequestListResponseBody, status_code=status.HTTP_200_OK)
async def find_review_list_from_student(request: Request, db: DbDependency, mentor_id: int):
    """
    受講生のレビュー一覧取得
    
    Parameter
    -----------------------
    mentor_id: int
        取得するメンターのユーザーID

    Returns
    -----------------------
    reviews: array
        id: int
            レビューのID
        title: str
            レビューのタイトル
        content: str
            レビューの内容
        curriculum_id: int
            レビューに紐づくカリキュラムのID
        tech_category: str
            カリキュラムのコースに紐づいた技術カテゴリ
        created_at:str
            レビューの作成日（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
    """
    review_requests = mentors_crud.find_review_requests_by_mentor_id(db, mentor_id)

    li = []
    for review_request in review_requests:
        # review_requestからcurriculumを取得し、curriculumに紐づくsectionを取得、sectionに紐づくcourseを取得、courseに紐づくtech_categoryを取得
        tech_category = mentors_crud.find_category_by_curriculum_id(db, review_request.curriculum_id)
        notifications = mentors_crud.find_notification_by_question_id(db, review_request.id)
        is_read = all([notification.is_read for notification in notifications])

        di = {
            "id": review_request.id,
            "title": review_request.title,
            "content": review_request.content,
            "curriculum_id": review_request.curriculum_id,
            "tech_category": tech_category.name,
            "created_at": review_request.created_at.isoformat(),
            "is_read": is_read,
            "is_closed": review_request.is_closed
        }

        li.append(di)

    return {"reviews": li}

@router.get("/counts", response_model=MentorsCountListResponseBody, status_code=status.HTTP_200_OK)
async def find_student_count(db: DbDependency):
    """
    メンター担当受講生数取得
    
    Parameter
    -----------------------
    なし

    Returns
    -----------------------
    mentors: array
        mentor_id: int
            メンターの一意識別子
        mentor_name: str
            メンターの名前
        student_content: str
            そのメンターが担当する受講生の数
    """

    mentors = mentors_crud.find_mentor_by_students(db)
    return mentors