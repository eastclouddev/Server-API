from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.account_get_detail import Responsebody
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger
from cruds import account_get_detail as account_get_detai_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=Responsebody, status_code=status.HTTP_200_OK)
async def merge_dicts(db: DbDependency, user_id: int = Path(gt=0)):
    user = account_get_detai_crud.find_by_user(db,user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    role = account_get_detai_crud.find_by_role(db,user.role_id)
    
    merged_dict = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "first_name_kana": user.first_name_kana,
        "last_name_kana": user.last_name_kana,
        "email": user.email,
        "role": role.name,
        "last_login": user.last_login.isoformat()
        }

    return  merged_dict