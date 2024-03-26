from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from logging import getLogger
from typing import Annotated
from database.database import get_db
from schemas.companies import  AllResponseBody
from cruds import companies as companies_crud
from services import companies as compamies_service

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/companies", tags=["CompaniesList"])


@router.get("",response_model=AllResponseBody, status_code=status.HTTP_200_OK)
def get_companies(db: DbDependency):

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

    found_companies = companies_crud.find_companies(db)

    if not found_companies:
        raise HTTPException(status_code=500,detail="Internal server error.")
    
    return compamies_service.create_companies_list(found_companies)