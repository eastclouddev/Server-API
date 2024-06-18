from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.mentors import QuestionListResponseBody, ProgressListResponseBody, ReviewRequestListResponseBody, MentorsCountListResponseBody, NotificationListResponseBody
from cruds import mentors as mentors_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])


@router.get("/{mentor_id}/progresses", response_model=ProgressListResponseBody, status_code=status.HTTP_200_OK)
async def find_progress_list_mentor(db: DbDependency, mentor_id: int, name: str = "", company: str = ""):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    検索
        name: str
        company: str

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

    students = mentors_crud.find_students_by_mentor_id(db, mentor_id)
    student_id_list = []
    companies = mentors_crud.find_companies_by_name(db, company)
    company_id_list = [com.id for com in companies]
    for student in students:
        user = mentors_crud.find_user_by_id(db, student.student_id)
        if any([
            name and (name in user.first_name),
            name and (name in user.last_name),
            name and (name in user.first_name_kana),
            name and (name in user.last_name_kana),
            name and (name in (user.last_name + user.first_name)),
            name and (name in (user.last_name_kana + user.first_name_kana)),
            company and (user.company_id in company_id_list),
            name == "" and company == "" # 検索なし
        ]):
            student_id_list.append(user.id)
    
    course_progresses = mentors_crud.find_course_progresses_by_student_id_list(db, student_id_list)
    if not course_progresses:
        raise HTTPException(status_code=404, detail="progresses not found")

    li = []
    for progress in course_progresses:
        di = {
            "progress_id": progress.id,
            "user_id": progress.user_id,
            "course_id": progress.course_id,
            "section_id": mentors_crud.find_section_by_course_id(db, progress.course_id),
            "curriculum_id": mentors_crud.find_curriculum_by_course_id(db, progress.course_id),
            "progress_percentage": progress.progress_percentage,
            "status": mentors_crud.find_status_by_status_id(db, progress.status_id)
        }
        li.append(di)

    return {"progresses": li}

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

@router.get("/{mentor_id}/notifications", response_model=NotificationListResponseBody, status_code=status.HTTP_200_OK)
async def find_notification(db: DbDependency, mentor_id: int):

    """
    通知一覧（メンター）
    
    Parameters
    -----------------------
    mentor_id:int
        ユーザーのID
    Returns
    -----------------------
    notifications: array
        id: int
            通知のID
        from_user: dict
            id: int
                通知を送ったユーザーのID
            name: str
                通知を送ったユーザーの名前
        question_id: int
            質問のID
        answer_id: int
            回答のID
        review_request_id: int
            レビューリクエストのID
        review_respomse_id: int
            レビューリスポンスのID
        title: str
            通知のタイトル
        content: str
            通知の内容
        is_read: bool
            通知が既読かどうか
        created_at: str
            通知が生成された日時（ISO 8601形式）

    explanation
    -----------------------
    メンターが受け取る通知は受講生の質問・回答・レビュー依頼・レビュー回答
    """
    
    # 自分宛ての通知を取得
    notifications = mentors_crud.find_notifications_by_mentor_id(db, mentor_id)

    # 返却データ作成
    li = []
    for i, notification in enumerate(notifications):
        q_id = None
        a_id = None
        req_id = None
        res_id = None
        title = ""
        content = ""

        # 質問・回答
        if notification.question_id:
            question = mentors_crud.find_question_by_question_id(db, notification.question_id)
            q_id = question.id
            title = question.title
            content = question.content
        elif notification.answer_id:
            answer = mentors_crud.find_answer_by_answer_id(db, notification.answer_id)
            question = mentors_crud.find_question_by_question_id(db, answer.question_id)
            q_id = question.id
            a_id = answer.id
            title = question.title
            content = answer.content
        # レビューリクエスト・レビューレスポンス
        elif notification.review_request_id:
            request = mentors_crud.find_request_by_request_id(db, notification.review_request_id)
            req_id = request.id
            title = request.title
            content = request.content
        elif notification.review_response_id:
            response = mentors_crud.find_response_by_response_id(db, notification.review_response_id)
            request = mentors_crud.find_request_by_request_id(db, response.review_request_id)
            req_id = request.id
            res_id = response.id
            title = request.title
            content = response.content

        user = mentors_crud.find_user_by_id(db, notification.from_user_id)
        di = {
            "id": i + 1,
            "from_user": {
                "id": notification.from_user_id,
                "name": user.last_name + user.first_name
            },
            "question_id": q_id,
            "answer_id": a_id,
            "review_request_id": req_id,
            "review_response_id": res_id,
            "title": title,
            "content": content,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat()
        }
        li.append(di)

    return {"notifications": li}