from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.billings import ResponseBilling
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import billings as billings
from logging import getLogger
from starlette import status

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/billings", tags=["Get_Detail"])


@router.get("/{billing_id}",status_code=status.HTTP_200_OK)
async def get_details(db: DbDependency, billing_id: int ):
    """
    請求履歴詳細取得

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
    info = billings.find_by_detail(db, billing_id)
    if not info:
        raise HTTPException(status_code=404, detail="Billing record not found")
    return info
