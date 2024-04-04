import jwt
import re
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.password_reset import PasswordResetRequest, PasswordResetConfirm
from cruds import password_reset as password_reset_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/password_reset", tags=["PasswordReset"])


@router.post("", status_code=status.HTTP_200_OK)
async def password_reset(db: DbDependency, param: PasswordResetRequest):
    user = password_reset_crud.find_by_email(db, param.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="Email address not found in the system.")
    
    # TODO:トークンを生成し、メールに送信する

    return

@router.post("/confirm", status_code=status.HTTP_200_OK)
async def password_setting(db: DbDependency, param: PasswordResetConfirm):
    try:
        # Token解析
        payload = jwt.decode(param.token, key='SECRET_KEY123', algorithms='HS256')
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")
        
        # パスワードのポリシー判定
        # 半角英数字、大文字小文字数字の混在、8文字以上14文字以下
        if any([
            not param.new_password,
            len(param.new_password) < 8,
            len(param.new_password) > 14,
            not re.match('.*[a-zA-Z]+.*', param.new_password),
            not re.match('.*[0-9]+.*', param.new_password)
        ]):
            raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")

        user = password_reset_crud.update_by_password(db, email, param.new_password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")

        db.commit()
        return {"message": "Your password has been reset successfully."}
    
    except jwt.ExpiredSignatureError as e: # 期限切れ
        logger.error(str(e))
        raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")

    except jwt.InvalidTokenError as e: # 無効なトークン
        logger.error(str(e))
        raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")

    except Exception as e:
        db.rollback()
        logger.error(str(e))
        raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")



