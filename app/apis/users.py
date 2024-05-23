from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.users import UserUpdateRequestBody, UserDetailResponseBody, UserListResponseBody, AccountListResponseBody
from cruds import users as users_crud
from services import users as users_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["Users"])


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(db: DbDependency, param: UserUpdateRequestBody, user_id: int = Path(gt=0)):
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
    duplication_user = users_crud.find_user_by_email(db, param.email, user_id)
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
	
@router.get("/{user_id}", response_model=UserDetailResponseBody, status_code=status.HTTP_200_OK)
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
    user = users_crud.find_user_by_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    role = users_crud.find_role_by_role_id(db, user.role_id)

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

@router.get("/{user_id}/email/confirm_change", status_code=status.HTTP_200_OK)
async def email_confirm_change(token, db: DbDependency, user_id: int = Path(gt=0),):
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
    found_user = users_crud.find_user_by_user_id(db, user_id)
    if not found_user:
        raise HTTPException(status_code = 400,detail="Invalid or expired token.")

    #アクセストークンからemailを取得
    token_info = users_service.get_email(token)

    try:
        # 該当のユーザーを更新
        update_info = users_crud.update_email(db, found_user, token_info)
        if not update_info:
            raise HTTPException(status_code = 400,detail="Invalid or expired token.")

        db.commit()
        return {"message": "Your email address has been successfully updated."}

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code = 400,detail="Invalid or expired token.")
    
@router.get("", response_model=UserListResponseBody, status_code=status.HTTP_200_OK)
async def find_student_list(db:DbDependency, role: str, page: int, limit: int):

    """
    受講生一覧(管理者)

    Parameters
    -----------------------
    role: str
        ユーザーの役割
    page: int
        取得するページ番号
    limit: int
        1ページ当たりの記事数

    Return
    -----------------------
    users: array
        user_id: int
            ユーザーのID
        first_name: str
            名前
        last_name: str
            姓
        email: str
            メールアドレス
        role: str
            ユーザーの役割
        last_login: str
            最終ログイン日時（ISO 8601形式）
    """

    users = users_crud.find_users_by_role(db, role)

    li = []

    for user in users[(page-1)*limit : page*limit]:
        di = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": role,
            "last_login": user.last_login.isoformat()
        }
        li.append(di)

    return {"users":li}

@router.get("/counts/", response_model=AccountListResponseBody, status_code=status.HTTP_200_OK)
async def find_number_of_accounts(db: DbDependency):
    """
    有効アカウント数取得

    Parameters
    -----------------------
    なし

    Return
    -----------------------
    role_counts: array
        role_id: int
            ロールのID
        role_name: str
            ロールの名称
        count: int
            そのロールを持つ有効なユーザーの総数
    """

    roles = users_crud.find_roles(db)
    li = []
    for role in roles:
        users = users_crud.find_users_by_role_id(db, role.id)
        di = {
            "role_id": role.id,
            "role_name": role.name,
            "count": len(users)
        }
        li.append(di)

    return {"role_counts": li}


