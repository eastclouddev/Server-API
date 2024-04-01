from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.companies import CreateRequestBody, CreateResponseBody, DetailResponseBody,AllResponseBody
from cruds import companies as companies_cruds
from services import companies as compamies_services

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=CreateResponseBody, status_code=status.HTTP_200_OK)
async def create_companies(db: DbDependency, param: CreateRequestBody):
    """
    会社情報作成

    Parameter
    -----------------------
    name: str
        会社名
    prefecture: str
        都道府県
    city: str
        市区町村
    town: str
        町名、番地等
    address: str
        建物名、部屋番号等
    postal_code: str
        郵便番号
    phone_number: str
        電話番号
    email: str
        メールアドレス

    Return
    ----------------------
    company_id: int
        新しく作成された会社のID
    name: str
        会社名
    prefecture: str
        都道府県
    city: str
        市区町村
    town: str
        町名、番地等
    address: str
        建物名、部屋番号等
    postal_code: str
        郵便番号
    phone_number: str
        電話番号
    email: str
        メールアドレス
    """

    try:
        new_company = companies_cruds.create_company(db, param)
        
        db.commit()
        
        re_di = {
            "company_id": new_company.id,
            "name": new_company.name,
            "prefecture": new_company.prefecture,
            "city": new_company.city,
            "town": new_company.town,
            "address": new_company.address,
            "postal_code": new_company.postal_code,
            "phone_number": new_company.phone_number,
            "email": new_company.email
        }

        return re_di
    
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    


@router.get("/{company_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_company_detail(db: DbDependency, company_id: int = Path(gt=0)):
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
    company_info = companies_cruds.find_by_company_id(db, company_id)
    if not company_info:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    info = {
        "company_id": company_id,
        "name": company_info.name,
        "prefecture": company_info.prefecture,
        "city": company_info.city,
        "town": company_info.town,
        "address": company_info.address,
        "postal_code": company_info.postal_code,
        "phone_number": company_info.phone_number,
        "email": company_info.email,
        "created_at": company_info.created_at.isoformat(),
        "updated_at": company_info.updated_at.isoformat()
    }

    return info



@router.get("",response_model=AllResponseBody, status_code=status.HTTP_200_OK)
async def find_companies(db: DbDependency):

    """
    会社情報一覧取得
    
    Parameters
    ----------
    なし

    Returns
    -------
    {"companies": companies_list} : dic{}
                    会社情報一覧
    
    """

    found_companies = companies_cruds.find_companies(db)

    if not found_companies:
        raise HTTPException(status_code=500,detail="Internal server error.")
    
    return compamies_services.create_companies_list(found_companies)