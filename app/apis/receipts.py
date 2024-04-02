from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.receipts import ResponseBody
from cruds import receipts as receipts_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/receipts", tags=["Receipts"])


@router.get("/{receipt_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_receipt_details(db: DbDependency, receipt_id: int = Path(gt=0)):
    """
    領収書出力
    Parameters
    ----------
    receipt_id: int
        出力する領収書のID

    Returns
    -------
    re_di: ResponseBody
        receipt_id, company_id, billing_id, date, amount, received_from, payment_method
    """

    company_receipt = receipts_crud.find_by_receipt_id(db, receipt_id)

    if not company_receipt:
        raise HTTPException(status_code=404, detail="Receipt not found.")
    
    company = receipts_crud.find_by_company_id(db, company_receipt.company_id)
    payment_method = receipts_crud.find_by_payment_method_id(db, company_receipt.payment_method_id)

    if not company or not payment_method:
        raise HTTPException(status_code=404, detail="Receipt not found.")

    re_di = {
        "receipt_id": company_receipt.id,
        "company_id": company_receipt.company_id,
        "billing_id": company_receipt.billing_info_id,
        "date": company_receipt.payment_date.strftime("%Y-%m-%d"),
        "amount": company_receipt.amount, # フロント側のNumber処理で.00は消えるので注意
        "received_from": company.name,
        "payment_method": payment_method.name
    }

    return re_di