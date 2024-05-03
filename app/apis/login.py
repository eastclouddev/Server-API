import hashlib
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.login import RequestBody, ResponseBody, LoginRequestBody
from cruds import login as login_crud
from services import login as login_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def login(db: DbDependency, param: LoginRequestBody):
    """
    ログイン認証
    
    Parameters
    -----------------------
    email: str
        ログインするユーザーのメールアドレス
    password: str
        ログインするユーザーのパスワード
    device_info: dict
        device_info: str
        device_name: str
        uuid: str

    Returns
    -----------------------
    dict
        user_id: int
            ログインしたユーザーのID
        access_token: str
            生成したトークン
        expires_in: int
            トークン有効期限
        role: str
            ユーザーのロール(役割)
    """

    # メールアドレスとパスワードで認証
    # TODO:ログインミスのカウント
    user = login_crud.find_user_by_email(db, param.email)
    password_sha256 = hashlib.sha256(param.password.encode()).hexdigest()
    if not user or user.password != password_sha256:
        logger.info("メールアドレスまたはパスワードの誤り")
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    # ユーザーのロールを取得    
    role = login_crud.find_role_by_role_id(db, user.role_id)
    
    # デバイスのチェック
    # 登録されているデバイスでのログインはOK
    # 2台目以降のデバイスでのログインはNG
    device = login_crud.find_device_by_user_id(db, user.id)
    if device:
        if device.device_type != param.device_info.device_type or device.device_name != param.device_info.device_name:
            logger.info("他のデバイスでログイン中")
            raise HTTPException(status_code=409, detail="User already logged in on another device.")

    # アクセストークンの生成
    access_token = login_service.create_access_token(user.id)

    # 返却データの作成
    re_di = {
        "user_id": user.id,
        "access_token": access_token,
        "expires_in": 3600,
        "role": role.name
    }

    return re_di



# @router.post("/old/", response_model=ResponseBody, status_code=status.HTTP_200_OK)
# async def login_old(db: DbDependency, request: RequestBody):
#     """
#     ログイン認証
    
#     Parameters
#     -----------------------
#     email: str
#         ログインするユーザーのメールアドレス
#     password: str
#         ログインするユーザーのパスワード
#     device_info: dict
#         device_info: str
#         device_name: str
#         uuid: str

#     Returns
#     -----------------------
#     dict
#         user_id: int
#             ログインしたユーザーのID
#         access_token: str
#             生成したトークン
#         expires_in: int
#             トークン有効期限
#         role: str
#             ユーザーのロール(役割)
#     """
#     # emailが一致するユーザーを取得
#     user = login_crud.find_by_user(db, request.email)
#     if not user:
#         logger.warning("userなし")
#         raise HTTPException(status_code=401, detail="Invalid email or password.")
    
#     # ユーザーから受けとったパスワードを暗号化
#     password_sha256 = hashlib.sha256(request.password.encode()).hexdigest()
#     if user.password != password_sha256:
#         logger.warning("パスワード不一致")
#         raise HTTPException(status_code=401, detail="Invalid email or password.")
    
#     # アクセストークンを生成する
#     access_token = login_service.create_access_token(user.id)
    
#     # 他のデバイスでログインできないようにする
#     user_device = login_crud.find_by_devices(db, user.id)
#     if user_device:
#         if user_device.device_type != request.device_info.device_type or user_device.device_name != request.device_info.device_name :
#             logger.warning("他のデバイスlogin中")
#             raise HTTPException(status_code=409, detail="User already logged in on another device.")
   
#     # ユーザーのロールを取得
#     role = login_crud.find_by_role(db, user.role_id)
#     if not role:
#         raise HTTPException(status_code=401, detail="Invalid email or password.")
    
#     return {
#             "user_id": user.id,
#             "access_token": access_token,
#             "expires_in": 3600,
#             "role": role.name
#         }