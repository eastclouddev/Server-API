import json
from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database.database import get_db
from logging import getLogger

from models.questions import Questions
from schemas.questions import RequestBody, ResponseBody
from cruds import questions as questions_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/curriculums", tags=["Questions"])

@router.post("/{curriculum_id}/questions", response_model=ResponseBody, status_code=status.HTTP_201_CREATED)
#関数.作成or送る(url),画面に返す型、成功した処理結果に出た数値)
async def get_receipt(db: DbDependency, param:RequestBody, curriculum_id: int = Path(gt=0)):
#複数の処理時の一斉スタート関数定義key (この関数内でデータベース操作、画面から受け取る型を関数置き換え、(0以上という条件された)パスパラメータ)
    
    found_curriculum = questions_crud.find_curriculum(db, curriculum_id)
    #引数を受け取ったcrudの関数を変数に置き換えた

    if not found_curriculum:
        raise HTTPException(status_code=404,detail="Curriculum not found.")
    #new_questionが見つからなかった場合の処理結果で"Curriculum not found."と画面に返ってくる

    di = {
            "url": param.media_content.url
        }
    media_json = json.dumps(di)

    try:
        new_question = questions_crud.create_question(db, param.user_id, param.title, param.content, media_json, curriculum_id)
        db.commit()
    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")     

    re_di = {
        "question_id": new_question.id,
        "curriculum_id": new_question.curriculum_id,
        "user_id": new_question.user_id,
        "title": new_question.title,
        "content": new_question.content,
        "media_content": [
            json.loads(new_question.media_content)
        ]
    }

    return re_di

