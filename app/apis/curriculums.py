from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.curriculums import ResponseBody
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import curriculums as get_detail
from logging import getLogger
from starlette import status


logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/curriculums", tags=["Get_Curriculm_Detail"])


@router.get("/{curriculum_id}",status_code=status.HTTP_200_OK)
# @router.get("/billings/{billing_id}",response_model= ResponseBilling)

async def get_details(db: DbDependency, curriculum_id: int ):
    """
    カリキュラム詳細取得

    Parameter
    -----------------------
    curriculum_id: int
        詳細を取得したいカリキュラムのID

    Return
    ----------------------
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
    info = get_detail.find_by_detail(db, curriculum_id)
    if not info:
        raise HTTPException(status_code=404, detail="Curriculum not found.")
    return info
