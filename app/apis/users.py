from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.users import UpdateRequestBody, Responsebody
from cruds import users as users_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["Users"])


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_account(db: DbDependency, param: UpdateRequestBody, user_id: int = Path(gt=0)):
	# メールアドレスの重複チェック
	duplication_user = users_crud.find_by_email(db, param.email, user_id)
	if duplication_user:
		raise HTTPException(status_code=400, detail="Email is already in use.")

	try:
		# 該当のユーザーを更新
		user = users_crud.update_by_user(db, param, user_id)
		if not user:
			raise Exception("NotUser")

		db.commit()
		return

	except Exception as e:
		db.rollback()
		logger.error(e)
		raise HTTPException(status_code=401, detail="Authentication failed.")
	
@router.get("/{user_id}", response_model=Responsebody, status_code=status.HTTP_200_OK)
async def find_user_detail(db: DbDependency, user_id: int = Path(gt=0)):
    user = users_crud.find_by_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    role = users_crud.find_by_role(db, user.role_id)
    
    re_di = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "first_name_kana": user.first_name_kana,
        "last_name_kana": user.last_name_kana,
        "email": user.email,
        "role": role.name,
        "last_login": user.last_login.isoformat()
    }

    return re_di