from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from cruds import mentors as mentors
from schemas.mentors import DetailResponseBody

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])



@router.get("/{mentor_id}/accounts",response_model=DetailResponseBody,status_code=status.HTTP_200_OK)

async def get_info(db: DbDependency, mentor_id: int ):
    """
    送金先の情報詳細を取得

    Parameter
    -----------------------
    mentor_id: int
        口座情報を取得したいメンターのID

        

    Return
    ----------------------
    mentor_id: int
        メンターのID
    account_name: str
        口座名義
    bank_name: str
        銀行名
    branch_name: str
        支店名
    account_number: str
        口座番号
    account_type: str
        口座の種類（例: "普通", "当座", "貯蓄"）

    

    """

    info = mentors.find_bank_info(db, mentor_id)
    if not info:
        raise HTTPException(status_code=404, detail="Mentor not found.")
    return info