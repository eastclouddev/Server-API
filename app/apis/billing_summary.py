from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.billing_summary import BillingSummaryResponseBody
from cruds import billing_summary as billing_summary_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/billing_summary", tags=["BillingSummary"])

@router.get("/last_month", response_model=BillingSummaryResponseBody, status_code=status.HTTP_200_OK)
async def find_billing_summary(db: DbDependency):
    """
    先月の請求金額合計取得

    Parameter
    -----------------------

    Returns
    -----------------------
    dict
        month: str
            対象月(ISO 8601形式)
        total_billed_amount: float
            先月の請求金額の合計
    """
    try:
        billing = billing_summary_crud.find_billing_summary(db)
        db.commit()
        return billing

    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid request or no data available for the specified month.")