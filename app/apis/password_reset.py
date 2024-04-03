import base64
import json
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
    # TODO:emailのフォーマットエラー
    
    if not user:
        logger.error("ユーザーが存在しません")
        raise HTTPException(status_code=404, detail="Email address not found in the system.")
    return {"message": "If an account with that email exists, we have sent a password reset email."}


@router.post("/confirm", status_code=status.HTTP_200_OK)
async def password_setting(db: DbDependency, param: PasswordResetConfirm):
    try:
        # Token解析
        token = param.token
        header, payload, signature = token.split('.')
        header = json.loads(base64.urlsafe_b64decode(header + '=' * (-len(header) % 4)).decode(encoding='utf-8'))
        payload = json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)).decode(encoding='utf-8'))

        # TODO:リセットトークンが無効かどうか、期限切れかどうかチェック

        # メールアドレスの取得
        email = payload.get("email")
        if not email:
            logger.error("メールアドレスが存在しません")
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
            logger.error("ユーザーが存在しません")
            raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")

        db.commit()
        return {"message": "Your password has been reset successfully."}
    
    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid token or password does not meet the security requirements.")



