from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.mentors import DetailResponseBody, ResponseBody, RequestBody
from cruds import mentors as mentors_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])



@router.get("/{mentor_id}/accounts",response_model=DetailResponseBody,status_code=status.HTTP_200_OK)
async def find_info_detail(db: DbDependency, mentor_id: int = Path(gt=0)):
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

    info = mentors_crud.find_bank_info(db, mentor_id)
    if not info:
        raise HTTPException(status_code=404, detail="Mentor not found.")
    return info


@router.post("/{mentor_id}/accounts", response_model=ResponseBody, status_code=status.HTTP_201_CREATED)
async def create_info(db: DbDependency, create_model: RequestBody, mentor_id: int = Path(gt=0)):

    """
        送金先の作成

    Parameter
    -----------------------
    mentor_id: int
        送金先情報を作成したいメンターのユーザーID
    bank_name: str 
        銀行名
    branch_name: str
        支店名
    bank_code: str 
        銀行コード
    branch_code: str 
        支店コード
    account_type: str 
        口座種別  ordinary (普通), current (当座), savings (貯蓄)
    account_number: str 
        口座番号 
    account_name: str 
        口座名義
        

    Return
    ----------------------
    account_id: int
        新しく作成された送金先情報のID
    mentor_id: int
        送金先情報を作成したいメンターのユーザーID
    bank_name: str 
        銀行名
    branch_name: str
        支店名
    bank_code: str 
        銀行コード
    branch_code: str 
        支店コード
    account_type: str 
        口座種別  ordinary (普通), current (当座), savings (貯蓄)
    account_number: str 
        口座番号 
    account_name: str 
        口座名義
    """

    new_transfer = mentors_crud.create(db, create_model,mentor_id)
    if not new_transfer:
        raise HTTPException(status_code=404, detail="Mentor not found.")

    try:
        db.commit()

        info = {
            "account_id": new_transfer.id,
            "mentor_id": mentor_id,
            "bank_name": new_transfer.bank_name,
            "branch_name": new_transfer.branch_name,
            "bank_code": new_transfer.bank_code,
            "branch_code": new_transfer.branch_code,
            "account_type": create_model.account_type,
            "account_number": new_transfer.account_number,
            "account_name": new_transfer.account_name
        }

    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    
    return info