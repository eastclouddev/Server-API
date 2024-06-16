from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.courses import CourseListResponseBody, CourseDetailResponseBody, CoursesStartRequestBody, CoursesStartResponsetBody,\
                            ReviewRequestCreateResponseBody, ReviewRequestCreateRequestBody, ReviewRequestListResponseBody,\
                            QuestionCreateResponseBody, QuestionCreateRequestBody, QuestionListResponseBody
from cruds import courses as courses_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", response_model=CourseListResponseBody, status_code=status.HTTP_200_OK)
async def find_course_list(db: DbDependency):
    """
    コース一覧取得

    Parameter
    -----------------------
    なし

    Returns
    -----------------------
    courses: array
        course_id: int
            コースのID
        title: str
            コースのタイトル
        description: str
            コースの説明
        created_user: int
            コースを作成したユーザーのID
        thumbnail_url: str
            コースのサムネイル画像のURL
        created_at: str
            コースの作成日時（ISO 8601形式）
    """

    courses = courses_crud.find_courses(db)

    li = []
    for course in courses:
        di = {
            "course_id": course.id,
            "title": course.title,
            "description": course.description,
            "created_user": course.created_user,
            "thumbnail_url": course.thumbnail_url,
            "created_at": course.created_at.isoformat()
        }
        li.append(di)

    re_di = {
        "courses": li
    }

    return re_di

@router.get("/{course_id}", response_model=CourseDetailResponseBody, status_code=status.HTTP_200_OK)
async def find_course_details(db: DbDependency, course_id: int = Path(gt=0)):
    """
    コース詳細取得

    Parameter
    -----------------------
    course_id: int
        取得するコースのID

    Returns
    -----------------------
    dict
        course_id: int
            コースのID
        title: str
            コースのタイトル
        description: str
            コースの詳細な説明
        created_user_id: int
            コースを作成したユーザーのID
        created_at: str
            コースの作成日時（ISO 8601形式）
        sections: array
            コースのセクション一覧
            section_id: int
                セクションのID
            title: str
                セクションのタイトル
            description: str
                セクションの説明
            curriculums: array
                セクションに紐づくカリキュラムの一覧
                curriculum_id: int
                    カリキュラムのID
                title: str
                    カリキュラムのタイトル
                description: str
                    カリキュラムの説明
    """
    course = courses_crud.find_course_by_course_id(db, course_id)
    sections = courses_crud.find_sections_by_course_id(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    section_li = []
    if sections:
        for section in sections:
            curriculums = courses_crud.find_curriculums_by_section_id(db, section.id)
            curriculum_li = []
            # 最内のリストを作成
            for curriculum in curriculums:
                curriculum_di = {
                    "curriculum_id": curriculum.id,
                    "title": curriculum.title,
                    "description": curriculum.description
                }
                curriculum_li.append(curriculum_di)

            section_di = {
                "section_id": section.id,
                "title": section.title,
                "description": section.description,
                "curriculums": curriculum_li
            }
            section_li.append(section_di)
    
    re_di = {
        "course_id": course.id,
        "title": course.title,
        "description": course.description,
        "created_user_id": course.created_user,
        "created_at": course.created_at.isoformat(),
        "sections": section_li
    }
	
    return re_di

@router.post("/start/", response_model=CoursesStartResponsetBody, status_code=status.HTTP_201_CREATED)
async def courses_start(db: DbDependency, param: CoursesStartRequestBody):
    """
    コース開始

    Parameter
    -----------------------
    user_id: int
        コースを開始するユーザーのID
    course_ids: array[int]
        開始するコースのIDリスト

    Returns
    -----------------------
    courses: array
        course_id: int
            開始したコースのID
        started_at: str
            コースの開始日（ISO 8601形式）
    """

    # コースIDの存在チェック
    for course_id in param.course_ids:
        if not courses_crud.find_course_by_course_id(db, course_id):
            raise HTTPException(status_code=404, detail="Course ID(s) not found.")

    # コースの開始（進捗テーブルの作成）
    try:
        courses_crud.create_course_progress(db, param.user_id, param.course_ids)
        db.commit()
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid user ID or course IDs.")

    # 画面返却値の作成
    li = []
    created_course_progresses = courses_crud.find_course_progress(db, param.user_id, param.course_ids)
    for course_progress in created_course_progresses:
        di = {
            "course_id": course_progress.course_id,
            "started_at": course_progress.started_at.isoformat()
        }
        li.append(di)

    re_di = {
        "courses": li
    }

    return re_di

@router.post("/{course_id}/reviews", response_model=ReviewRequestCreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_review_request(db: DbDependency, param: ReviewRequestCreateRequestBody, course_id: int):
    """
    レビュー投稿
    
    Parameter
    -----------------------
    course_id: int
        レビューを取得したいコースのID
    dict
        curriculum_id: int
            レビューが紐づくカリキュラムのID
        user_id: int
            ユーザーのID
        title: str
            レビューリクエストのタイトル
        content: str 
            レビューリクエストの内容
        media_content: dict
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL

    Returns
    -----------------------
    dict
        id: int
            レビューリクエストのID
        curriculum_id: int
            カリキュラムのID
        user: dict
            user_id: int
                レビューを投稿したユーザーのID
            name: str
                レビューを投稿したユーザーの名前
        title: str
            レビューリクエストのタイトル
        content: str 
            レビューリクエストの内容
        media_content: array
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
        created_at: str
            レビューが作成された日時（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            レビューリクエストがクローズされているかどうか
        reply_counts: int
            質問の返信数
    """

    found_curriculum = courses_crud.find_review_request_by_curriculum_id(db, param.curriculum_id)

    if not found_curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found.")
    
    li = []
    datas = param.media_content
    for data in datas:
        if hasattr(data, "url"):
            di = {
                "url": data.url
            }
            li.append(di)
    media_json = li

    try:
        reviews = courses_crud.create_review_request(db, param, media_json, course_id)
        db.commit()

        user = courses_crud.find_user_by_id(db, reviews.user_id)
        di = {
            "id": reviews.id,
            "curriculum_id": reviews.curriculum_id,
            "user": {
                "user_id": user.id,
                "name": user.last_name + user.first_name
            },
            "title": reviews.title,
            "content": reviews.content,
            "media_content": reviews.media_content,
            "created_at": reviews.created_at.isoformat(),
            "is_read": False, # 作成なので、この時点ではFalse確定
            "is_closed": False, # 作成なので、この時点ではFalse確定
            "reply_counts": 0 # 作成なので、この時点では0確定
        }
        
        return di
    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{course_id}/reviews", response_model=ReviewRequestListResponseBody, status_code=status.HTTP_200_OK)
async def find_review_list(db: DbDependency, course_id: int):
    """
    コースのレビュー一覧

    Parameter
    -----------------------
    course_id: int
        レビュー一覧を取得したいコースのID

    Returns
    -----------------------
    reviews: array
        id: int
            レビューリクエストのID
        user: dict
            user_id: int
                レビューを投稿したユーザーのID
            name: str
                レビューを投稿したユーザーの名前
        title: str
            レビューリクエストのタイトル
        content: str
            レビューリクエストの内容
        curriculum_id: int
            関連するカリキュラムのID
        created_at: str
            レビューリクエストが作成された日時（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            レビューリクエストがクローズされているかどうか
        reply_counts: int
            レビューの返信数
    """
    reviews = courses_crud.find_reviews_by_curriculum_id(db, course_id)

    li = []
    for review in reviews:
        user = courses_crud.find_user_by_id(db, review.user_id)
        notifications = courses_crud.find_notification_by_user_id_and_question_id(db, review.user_id, review.id)
        is_read = all([notification.is_read for notification in notifications])
        responses = courses_crud.find_response_by_request_id(db, review.id)

        di = {
            "id": review.id,
            "user": {
                "user_id": user.id,
                "name": user.last_name + user.first_name
            },
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "created_at": review.created_at.isoformat(),
            "is_read": is_read,
            "is_closed": review.is_closed,
            "reply_counts": len(responses)
        }
        li.append(di)

    re_di = {
        "reviews": li
    }

    return re_di

@router.post("/{course_id}/questions", response_model=QuestionCreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_question(db: DbDependency, param: QuestionCreateRequestBody, course_id: int):
    """
    質問投稿
    
    Parameter
    -----------------------
    course_id: int
        質問を投稿したいコースのID
    dict
        curriculum_id: int
            質問が紐づくカリキュラムのID
        user_id: int
            ユーザーのID
        title: str
            質問のタイトル
        objective: str
            学習内容で実践したこと
        current_situation: str
            現状
        research: str
            自分が調べたこと
        content: str 
            質問の内容
        media_content: str
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL

    Returns
    -----------------------
    dict
        question_id: int
            質問のID
        curriculum_id: int
            カリキュラムのID
        user: dict
            user_id: int
                質問を投稿したユーザーのID
            name: str
                質問を投稿したユーザーの名前
        title: str
            質問のタイトル
        objective: str
            学習内容で実践したこと
        current_situation: str
            現状
        research: str
            自分が調べたこと
        content: str 
            質問の内容
        media_content: dict
            関連するメディアコンテンツの情報
        created_at: str
            質問作成日（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
        reply_counts: int
            質問の返信数
    """
    found_curriculum = courses_crud.find_curriculum_by_curriculum_id(db, param.curriculum_id)

    if not found_curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found.")

    li = []
    datas = param.media_content
    for data in datas:
        if hasattr(data, "url"):
            di = {
                "url": data.url
            }
            li.append(di)
    media_json = li

    try:
        new_question = courses_crud.create_question(db, course_id, param, media_json)
        db.commit()

        user = courses_crud.find_user_by_id(db, new_question.user_id)
        
        re_di = {
            "question_id": new_question.id,
            "curriculum_id": new_question.curriculum_id,
            "user": {
                "user_id": user.id,
                "name": user.last_name + user.first_name
            },
            "title": new_question.title,
            "objective": new_question.objective,
            "current_situation": new_question.current_situation,
            "research": new_question.research,
            "content": new_question.content,
            "media_content": new_question.media_content,
            "created_at": new_question.created_at.isoformat(),
            "is_read": False, # 作成なので、この時点ではFalse確定
            "is_closed": False, # 作成なので、この時点ではFalse確定
            "reply_counts": 0 # 作成なので、この時点では0確定
        }

        return re_di

    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{course_id}/questions", response_model=QuestionListResponseBody, status_code=status.HTTP_200_OK)
async def find_question_list_in_curriculum(db: DbDependency, course_id: int):
    """
    コースの質問一覧
    
    Parameter
    -----------------------
    course_id: int
        質問一覧を取得したいコースのID

    Returns
    -----------------------
    questions: array
        question_id: int
            質問のID
        user: dict
            user_id: int
                質問を投稿したユーザーのID
            name: str
                質問を投稿したユーザーの名前
        title: str
            質問のタイトル
        content: str 
            質問の内容
        curriculum_id: int
            カリキュラムのID
        created_at: str
            質問作成日（ISO 8601形式）
        is_read: bool
            未読コメントの有無
        is_closed: bool
            完了しているかどうか
        reply_counts: int
            質問の返信数
    """

    questions = courses_crud.find_questions_by_course_id(db, course_id)

    if not questions:
        raise HTTPException(status_code=404, detail="Questions not found for the specified curriculum.")

    li = []
    for question in questions:
        # TODO:不要?
        # media_content_list = []
        # datas = question.media_content
        # for data in datas:
        #     if "url" in data:
        #         di = {
        #             "url": data.get("url", "")
        #         }
        #         media_content_list.append(di)
        
        user = courses_crud.find_user_by_id(db, question.user_id)
        notifications = courses_crud.find_notification_by_user_id_and_question_id(db, question.user_id, question.id)
        is_read = all([notification.is_read for notification in notifications])
        answers = courses_crud.find_answers_by_question_id(db, question.id)
        di = {
            "question_id": question.id,
            "user": {
                "user_id": user.id,
                "name": user.last_name + user.first_name
            },
            "title": question.title,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "created_at": question.created_at.isoformat(),
            "is_read": is_read,
            "is_closed": question.is_closed,
            "reply_counts": len(answers)
            # "media_content": media_content_list
        }
        li.append(di)
    
    re_di = {
        "questions": li
    }
    return re_di