from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger

from schemas.users import UserUpdate
from cruds import users as account_update_cruds

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["Users"])


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_account(db: DbDependency, param: UserUpdate, user_id: int = Path(gt=0)):
        # メールアドレスの重複チェック
        duplication_user = account_update_cruds.find_by_email(db, param.email, user_id)
        if duplication_user:
            raise HTTPException(status_code=400, detail="Email is already in use.")

        try:
            # 該当のユーザーを更新
            user = account_update_cruds.update_by_user(db, param, user_id)
            if not user:
                raise Exception("NotUser")

            db.commit()
            return

        except Exception as e:
            db.rollback()
            logger.error(e)
            raise HTTPException(status_code=401, detail="Authentication failed.")

