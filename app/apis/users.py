from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.users import UserCreate, UserResponse
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import users as users_crud
from logging import getLogger

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(db: DbDependency, user_create: UserCreate):
    try:
        new_user = users_crud.create(db, user_create)
        db.commit()
    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed user create")
    return new_user