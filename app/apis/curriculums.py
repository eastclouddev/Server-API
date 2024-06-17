from logging import getLogger
from typing import Annotated
import json

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.curriculums import CurriculumDetailResponseBody
from cruds import curriculums as curriculums_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/curriculums", tags=["Curriculums"])


@router.get("/{curriculum_id}", response_model=CurriculumDetailResponseBody, status_code=status.HTTP_200_OK)
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
        is_quiz: boolean
            このカリキュラムがテストかどうかを示すフラグ（boolean）
        quiz_content: array
            quiz_id: int
                テストのID
            question: str
                問題文
            media_content: str
                メディアコンテンツのURL
            options: array
                選択肢
            correct_answer: int
                正しい回答
            explanation: str
                正解にする説明
        display_no: int
            カリキュラムの表示順
    """
    info = curriculums_crud.find_info_by_curriculum_id(db, curriculum_id)
    if not info:
        raise HTTPException(status_code=404, detail="Curriculum not found.")
    return info


# @router.get("/{curriculum_id}/test", response_model=QuizDetailResponseBody, status_code=status.HTTP_200_OK)
# async def find_test_details(db: DbDependency, curriculum_id: int = Path(gt=0)):
#     """
#     テスト詳細取得
#     Parameter
#     -----------------------
#     curriculum_id: int
#         テストを取得したいカリキュラムのID
#     Returns
#     -----------------------
#     dict
#         curriculum_id: int
#             カリキュラムのID
#         tests: array
#             test_id: int
#                 テストのID
#             question: str
#                 質問文
#             options: array of str
#                 選択肢
#             correct_answer: str
#                 正解の選択肢
#             explanation: str
#                 正解の解説
#             media_content_url: str
#                 メディアコンテンツのURL
#     """
#     quizzes = curriculums_crud.find_quiz_contents_by_curriculum_id(db, curriculum_id)
#     if not quizzes:
#         raise HTTPException(status_code=404, detail="Test content not found for the specified curriculum.")
#     li = []
#     for quiz in quizzes:
#         option_list = []
#         for option in quiz.options.values():
#             option_list.append(option)
#         url_list = []
#         for media_content in quiz.media_content:
#             if "url" in media_content:
#                 url_list.append(media_content.get("url", ""))
#         di = {
#             "test_id": quiz.id,
#             "question": quiz.question,
#             "options": option_list,
#             "correct_answer": quiz.correct_answer,
#             "explanation": quiz.explanation,
#             "media_content_url": url_list
#         }
#         li.append(di)
#     re_di = {
#         "curriculum_id": curriculum_id,
#         "tests": li
#     }
#     return re_di
