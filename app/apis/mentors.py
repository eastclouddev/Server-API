from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.mentors import ResponseBodyGet
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import mentors as mentors
from logging import getLogger
from starlette import status

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/mentors", tags=["Get_Transfer"])


@router.get("/{mentor_id}/accounts",status_code=status.HTTP_200_OK)

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
