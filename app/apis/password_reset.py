from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/password_reset", tags=["PasswordReset"])


@router.post("", status_code=status.HTTP_200_OK)
async def reset(db: DbDependency):
	return {}


@router.post("/confirm", status_code=status.HTTP_200_OK)
async def confirm(db: DbDependency):
	return {}