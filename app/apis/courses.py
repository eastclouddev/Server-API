from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.courses import CourseListResponseBody, CourseDetailResponseBody, CoursesStartRequestBody, CoursesStartResponsetBody
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
        expectesd_end_hours: int
            コースの終了想定時間
        total_curriculums: int
            カリキュラム総数
        tech_category: str
            技術カテゴリ
        created_at: str
            コースの作成日時（ISO 8601形式）
    """

    courses = courses_crud.find_courses(db)

    li = []
    for course in courses:
        curriculums = courses_crud.find_curriculums_by_course_id(db, course.id)
        tech_category = courses_crud.find_tech_category_by_category_id(db, course.tech_category_id)
        di = {
            "course_id": course.id,
            "title": course.title,
            "description": course.description,
            "created_user": course.created_user,
            "thumbnail_url": course.thumbnail_url,
            "expected_end_hours": course.expected_end_hours,
            "total_curriculums": len(curriculums),
            "tech_category": tech_category.name,
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
        thumbnail_url: str
            コースのサムネイル画像のURL
        expectesd_end_hours: int
            コースの終了想定時間
        total_curriculums: int
            カリキュラム総数
        tech_category: str
            技術カテゴリ
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
            duration: str
                セクションの時間（HH:MM:SS形式）
            curriculums: array
                セクションに紐づくカリキュラムの一覧
                curriculum_id: int
                    カリキュラムのID
                title: str
                    カリキュラムのタイトル
                description: str
                    カリキュラムの説明
                duration: str
                    セクションの時間（HH:MM:SS形式）
                is_completed: bool
                    カリキュラム完了状況
    """
    course = courses_crud.find_course_by_course_id(db, course_id)
    sections = courses_crud.find_sections_by_course_id(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    section_li = []
    if sections:
        for section in sections:
            curriculums = courses_crud.find_curriculums_by_section_id(db, section.id)
            tech_category = courses_crud.find_tech_category_by_category_id(db, course.tech_category_id)

            curriculum_li = []
            # 最内のリストを作成
            for curriculum in curriculums:
                curriculum_progresses = courses_crud.find_curriculums_progress_by_curriculum_id(db, curriculum.id)
                # duration:動画時間の秒数を"00:00:00"の形で返す
                hours = curriculum.duration / 3600
                minutes = (curriculum.duration % 3600) / 60
                seconds = (curriculum.duration % 60)
                curriculum_duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                curriculum_di = {
                    "curriculum_id": curriculum.id,
                    "title": curriculum.title,
                    "description": curriculum.description,
                    "duration": curriculum_duration,
                    "is_completed": curriculum_progresses.is_completed
                }
                curriculum_li.append(curriculum_di)
            
            # duration:動画時間の秒数を"00:00:00"の形で返す
            hour = section.duration / 3600
            minute = (section.duration % 3600) / 60
            second = (section.duration % 60)
            section_duration = f"{int(hour):02}:{int(minute):02}:{int(second):02}"
            section_di = {
                "section_id": section.id,
                "title": section.title,
                "description": section.description,
                "duration": section_duration,
                "curriculums": curriculum_li
            }
            section_li.append(section_di)
        
        re_di = {
            "course_id": course.id,
            "title": course.title,
            "description": course.description,
            "created_user_id": course.created_user,
            "thumbnail_url": course.thumbnail_url,
            "expected_end_hours": course.expected_end_hours,
            "total_curriculums": len(curriculums),
            "tech_category": tech_category.name,
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