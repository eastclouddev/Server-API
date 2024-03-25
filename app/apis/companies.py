from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.companies import RequestBody, ResponseBody
from cruds import companies as companies_cruds

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def create_companies(db: DbDependency, param: RequestBody):

    try:
        new_company = companies_cruds.create(db, param)
        
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