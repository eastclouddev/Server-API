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
        content: str
            質問の内容
        curriculum_id: str
            質問が紐づくカリキュラムのID
        created_at: str
            質問作成日
        is_read: str
            未読コメントの有無
        is_closed: str
            完了しているかどうか
    """
	
    # TODO:ヘッダー情報をどう使うか
    header = request.headers
	
    questions = mentors_crud.find_questions_by_mentor_id(db, mentor_id)

    li = []
    for question in questions:
        answers = mentors_crud.find_answers_by_question_id(db, question.id)
        read_flag = all([answer.is_read for answer in answers]) # 全てtrueだった場合にはtrue、1つでもfalseがあればfalse
        
        di = {
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "created_at": question.created_at.isoformat(),
            "is_read": read_flag,
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
        created_at:str
            レビューの作成日（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
    """
    found_reviews = mentors_crud.find_review_requests_by_user_id(db, mentor_id)
    reviews_list = []

    for review in found_reviews:
        one_review = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "created_at": review.created_at.isoformat(),
            "is_read": True, #TODO テーブル変更のため
            "is_closed": review.is_closed
        }

        reviews_list.append(one_review)

    return {"reviews": reviews_list}

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