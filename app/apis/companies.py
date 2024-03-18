from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.companies import CompanyUpdate, CompanyResponse
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import companies as company_crud
from logging import getLogger

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.put("/{id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def update(
    db: DbDependency,
    company_update: CompanyUpdate,
    id: int = Path(gt=0),
):
    existing_company = company_crud.find_by_id(db, id)
    if not existing_company:
        raise HTTPException(status_code=404, detail="Company not found")
    try:
        updated_company = company_crud.update(db, id, company_update)
        db.commit()
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update company")
    return updated_company