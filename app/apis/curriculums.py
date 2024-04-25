from logging import getLogger
from typing import Annotated
import json

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.curriculums import ReviewsResponseBody, DetailResponseBody, RequestBody, ResponseBody,\
                                ReviewResponse, ReviewRequestBody, QuizResponseBody, QuestionResponseBody
from cruds import curriculums as curriculums_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/curriculums", tags=["Curriculums"])

@router.get("/{curriculum_id}/reviews", response_model=ReviewsResponseBody, status_code=status.HTTP_200_OK)
async def find_review_list(db: DbDependency, curriculum_id: int = Path(gt=0)):
    """
    カリキュラムのレビュー一覧

    Parameter
    -----------------------
    curriculum_id: int
        レビュー一覧を取得したいカリキュラムのID

    Returns
    -----------------------
    reviews: array
        id: int
            レビューリクエストのID
        curriculum_id: int
            関連するカリキュラムのID
        user_id: int
            レビューリクエストを投稿したユーザーのID
        title: str
            レビューリクエストのタイトル
        content: str
            レビューリクエストの内容
        is_closed: bool
            レビューリクエストがクローズされているかどうか
        created_at: str
            レビューリクエストが作成された日時（ISO 8601形式）
        updated_at: str
            レビューリクエストが最後に更新された日時（ISO 8601形式）
    """

    reviews = curriculums_crud.find_reviews(db, curriculum_id)

    li = []
    for review in reviews:
        di = {
            "id": review.id,
            "curriculum_id": review.curriculum_id,
            "user_id": review.user_id,
            "title": review.title,
            "content": review.content,
            "is_closed": review.is_closed,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        }
        li.append(di)

    re_di = {
        "reviews": li
    }

    return re_di

@router.get("/{curriculum_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_curriculum_details(db: DbDependency, curriculum_id: int = Path(gt=0)):
    """
    カリキュラム詳細取得

    Parameter
    -----------------------
    curriculum_id: int
        詳細を取得したいカリキュラムのID

    Returns
    -----------------------
    dict
        curriculum_id: int
            カリキュラムのID
        title: str
            カリキュラムのタイトル
        description: str
            カリキュラムの詳細な説明
        video_url: str
            ビデオコンテンツのURL(ビデオが存在する場合のみ）
        content: str 
            カリキュラムのテキストコンテンツ(テキストコンテンツが存在する場合のみ）
        is_test: boolean
            このカリキュラムがテストかどうかを示すフラグ（boolean）
        display_no: int
            カリキュラムの表示順
    """
    info = curriculums_crud.find_by_curriculum_id(db, curriculum_id)
    if not info:
        raise HTTPException(status_code=404, detail="Curriculum not found.")
    return info


@router.get("/{curriculum_id}/test", response_model=QuizResponseBody, status_code=status.HTTP_200_OK)
async def find_test_details(db: DbDependency, curriculum_id: int = Path(gt=0)):
    """
    テスト詳細取得
    Parameter
    -----------------------
    curriculum_id: int
        テストを取得したいカリキュラムのID
    Returns
    -----------------------
    dict
        curriculum_id: int
            カリキュラムのID
        tests: array
            test_id: int
                テストのID
            question: str
                質問文
            options: array of str
                選択肢
            correct_answer: str
                正解の選択肢
            explanation: str
                正解の解説
            media_content_url: str
                メディアコンテンツのURL
    """
    quizzes = curriculums_crud.find_quiz_contents(db, curriculum_id)
    if not quizzes:
        raise HTTPException(status_code=404, detail="Test content not found for the specified curriculum.")
    li = []
    for quiz in quizzes:
        option_list = []
        for option in quiz.options.values():
            option_list.append(option)
        url_list = []
        for media_content in quiz.media_content:
            if "url" in media_content:
                url_list.append(media_content.get("url", ""))
        di = {
            "test_id": quiz.id,
            "question": quiz.question,
            "options": option_list,
            "correct_answer": quiz.correct_answer,
            "explanation": quiz.explanation,
            "media_content_url": url_list
        }
        li.append(di)
    re_di = {
        "curriculum_id": curriculum_id,
        "tests": li
    }
    return re_di

@router.post("/{curriculum_id}/questions", response_model=ResponseBody, status_code=status.HTTP_201_CREATED)
async def create_question(db: DbDependency, param:RequestBody, curriculum_id: int = Path(gt=0)):
    """
    質問投稿作成取得
    
    Parameter
    -----------------------
    curriculum_id: int
        詳細を取得したいカリキュラムのID
    dict
        user_id: int
            ユーザーのID
        title: str
            質問のタイトル
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
        user_id: int
            ユーザーのID
        title: str
            質問のタイトル
        content: str 
            質問の内容
        media_content: str 
            関連するメディアコンテンツの情報
    """
    found_curriculum = curriculums_crud.find_curriculum(db, curriculum_id)

    if not found_curriculum:
        raise HTTPException(status_code=404,detail="Curriculum not found.")

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
        new_question = curriculums_crud.create_question(db, param.user_id, param.title, param.content, media_json, curriculum_id)
        db.commit()
        
        re_di = {
            "question_id": new_question.id,
            "curriculum_id": new_question.curriculum_id,
            "user_id": new_question.user_id,
            "title": new_question.title,
            "content": new_question.content,
            "media_content": new_question.media_content
        }

        return re_di

    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{curriculum_id}/questions", response_model= QuestionResponseBody, status_code=status.HTTP_200_OK)
async def find_question_list_in_curriculum(db: DbDependency, curriculum_id: int):
    """
    カリキュラムの質問一覧
    
    Parameter
    -----------------------
    curriculum_id: int
        質問一覧を取得したいカリキュラムのID

    Returns
    -----------------------
    dict
        question_id: int
            質問のID
        curriculum_id: int
            カリキュラムのID
        user_id: int
            ユーザーのID
        title: str
            質問のタイトル
        content: str 
            質問の内容
        media_content: str
            関連するメディアコンテンツの情報
            url: str
                メディアコンテンツのURL
    """

    questions = curriculums_crud.find_by_questions(db, curriculum_id)

    if not questions:
        raise HTTPException(status_code=404, detail="Questions not found for the specified curriculum.")

    li = []
    for question in questions:
        media_content_list = []

        datas = question.media_content
        
        for data in datas:
            if "url" in data:
                di = {
                    "url": data.get("url", "")
                }
                media_content_list.append(di)
        
        di = {
            "question_id": question.id,
            "curriculum_id": question.curriculum_id,
            "user_id": question.user_id,
            "title": question.title,
            "content": question.content,
            "media_content": media_content_list
        }
        li.append(di)
    
    re_di = {
        "questions": li
    }
    return re_di


@router.post("/{curriculum_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(db: DbDependency, param: ReviewRequestBody, curriculum_id: int):

    """
    レビュー作成
    
    Parameter
    -----------------------
    curriculum_id: int
        詳細を取得したいカリキュラムのID
    dict
        user_id: int
            ユーザーのID
        title: str
            レビューリクエストのタイトル
        content: str 
            レビューリクエストの内容
        is_closed: boolean
            レビューリクエストの初期状態（通常はfalseで未クローズ状態）
     Returns
    -----------------------
    dict
        id: int
            レビューリクエストのID
        curriculum_id: int
            カリキュラムのID
        user_id: int
            ユーザーのID
        title: str
            レビューリクエストのタイトル
        content: str 
            レビューリクエストの内容
        is_closed: boolean
            レビューリクエストがクローズされているかどうか（boolean）
        created_at: str
            作成された日時
    """


    found_curriculum = curriculums_crud.find_by_reviews(db,curriculum_id)

    if not found_curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found.")

    try:
        reviews = curriculums_crud.create_reviews(db, curriculum_id, param.user_id, param.title, param.content, param.is_closed)
        db.commit()
        di = {
            "id": reviews.id,
            "curriculum_id": reviews.curriculum_id,
            "user_id": reviews.user_id,
            "title": reviews.title,
            "content": reviews.content,
            "is_closed": reviews.is_closed,
            "created_at": reviews.created_at.isoformat()
        }
        
        return di
    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.") 
