from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.companies import ResponseBody
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import companies as companies
from logging import getLogger
from starlette import status

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/companies", tags=["Get_Company_Detail"])


@router.get("/{company_id}",status_code=status.HTTP_200_OK)

async def get_details(db: DbDependency, company_id: int ):
    """
    会社詳細取得

    Parameter
    -----------------------
    company_id: int
        詳細情報を取得したい会社のID

    Return
    ----------------------
    company_id: int
        会社のID（
    name: str
        会社の名前
    prefecture: str
        所在地の都道府県
    city: str
        所在地の市区町村
    town: str
        所在地の町名・番地等
    address: str
        会社の詳細な住所
    postal_code: str
        郵便番号
    phone_number: str
        電話番号
    email: str
        会社のメールアドレス
    created_at: str
        レコードの作成日時（ISO 8601形式）
    updated_at: str
        レコードの最終更新日時（ISO 8601形式）

    """
    info = companies.find_by_detail(db, company_id)
    if not info:
        raise HTTPException(status_code=404, detail="Company not found.")
    return info
