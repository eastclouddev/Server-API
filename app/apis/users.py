from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.users import UpdateRequestBody, DetailResponseBody, EmailRequestBody
from cruds import users as users_crud
from services import users as users_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["Users"])


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(db: DbDependency, param: UpdateRequestBody, user_id: int = Path(gt=0)):
    """
    アカウント更新

    Parameters
    -----------------------
    dict
        first_name: str
            名前
        last_name: str
            姓
        first_name_kana: str
            名前（カナ）
        last_name_kana: str
            姓（カナ）
        email: str
            メールアドレス
    user_id: int
        更新するユーザーのID

    Returns
    -----------------------
    なし
    """
    # メールアドレスの重複チェック
    duplication_user = users_crud.find_by_email(db, param.email, user_id)
    if duplication_user:
        raise HTTPException(status_code=400, detail="Email is already in use.")

    try:
        # 該当のユーザーを更新
        user = users_crud.update_user(db, param, user_id)
        if not user:
            raise Exception("NotUser")

        db.commit()
        return

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code=401, detail="Authentication failed.")
	
@router.get("/{user_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
async def find_user_details(db: DbDependency, user_id: int = Path(gt=0)):
    """
    アカウント詳細取得

    Parameter
    -----------------------
    user_id: int
        取得するユーザーのID

    Returns
    -----------------------
    dict
        user_id: str
            取得したユーザーのID
        first_name: str
            名前
        last_name: str
            姓
        first_name_kana: str
            名前（カナ）
        last_name_kana: str
            姓（カナ）
        email: str
            メールアドレス
        role: str
            ユーザーのロール
        last_login: str
            最終ログイン日時（ISO 8601形式）
    """
    user = users_crud.find_by_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    role = users_crud.find_by_role_id(db, user.role_id)

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


@router.post("/{user_id}/email/change_request", status_code=status.HTTP_200_OK)
async def confirm_change_email(db: DbDependency, new_email: EmailRequestBody, user_id: int = Path(gt=0)):
    """
    メールアドレス変更

    Parameters
    -----------------------
    user_id: int
        メールアドレスを変更するユーザーのID
    new_email: str
        新しく登録するメールアドレス

    Return
    -----------------------
    なし
    """

    # 登録したいメールアドレスが既に使われているかチェック
    user = users_crud.find_by_email(db, new_email, user_id)
    if user:
        raise HTTPException(status_code=400, detail="The email address is already in use.")

    # TODO:メールアドレスの更新前と更新後が同じ場合はどうするか？
    # TODO:トークンを生成し、メールが送信される

    return


@router.get("/{user_id}/email/confirm_change", status_code=status.HTTP_200_OK)
async def confirm_change_email(token, db: DbDependency, user_id: int = Path(gt=0)):
    """
    メールアドレス認証と更新

    Parameters
    -----------------------
    user_id: int
        メールアドレスを変更しようとしているユーザーのID
    token: str
        メールアドレス変更を認証するための一意のトークン

    Return
    -----------------------
    message: str
        "Your email address has been successfully updated."}
    """
    #一致するユーザーを取得
    found_user = users_crud.find_user(db,user_id)
    if not found_user:
        raise HTTPException(status_code = 400,detail="Invalid or expired token.")

    #アクセストークンからemailを取得
    token_info = users_service.get_email(token)

    try:
        # 該当のユーザーを更新
        update_info = users_crud.update_address(db,found_user,token_info)
        if not update_info:
            raise HTTPException(status_code = 400,detail="Invalid or expired token.")

        db.commit()
        return {"message": "Your email address has been successfully updated."}

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code = 400,detail="Invalid or expired token.")