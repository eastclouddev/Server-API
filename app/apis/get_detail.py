from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.get_detail import ResponseBilling
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import get_detail as get_detail
from logging import getLogger

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="", tags=["Get_Details_History"])


@router.get("/billings/{billing_id}")
# @router.get("/billings/{billing_id}",response_model= ResponseBilling)

async def get_details(db: DbDependency, billing_id: int ):
    """

    Parameter
    -----------------------
    billing_id: int


    Return
    ----------------------
    billing_id: int
        請求履歴のID
    company_id: int
        会社のID
    date: str
        請求日（YYYY-MM-DD形式）
    amount: float
        請求金額
    status: string
        請求状況（例: "paid", "unpaid", "overdue"）
    payment_details: 
        支払いの詳細（オプション、支払いが完了している場合に含まれる）
            payment_method: str
                支払い方法
            payment_date: str
                支払い日（YYYY-MM-DD形式）

    """
    info = get_detail.find_by_detail(db, billing_id)
    if not info:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return info
