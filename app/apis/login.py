import hashlib
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.login import RequestBody, ResponseBody
from cruds import login as login_crud
from services import login as login_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def login(db: DbDependency, request: RequestBody):
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
    # emailが一致するユーザーを取得
    user = login_crud.find_by_user(db, request.email)
    if not user:
        logger.warning("userなし")
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    # ユーザーから受けとったパスワードを暗号化
    password_sha256 = hashlib.sha256(request.password.encode()).hexdigest()
    if user.password != password_sha256:
        logger.warning("パスワード不一致")
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    # アクセストークンを生成する
    access_token = login_service.create_access_token(user.id)
    
    # 他のデバイスでログインできないようにする
    user_device = login_crud.find_by_devices(db, user.id)
    if user_device:
        if user_device.device_type != request.device_info.device_type or user_device.device_name != request.device_info.device_name :
            logger.warning("他のデバイスlogin中")
            raise HTTPException(status_code=409, detail="User already logged in on another device.")
    #　新規デバイス情報の作成
    else :
        try:
            new_device = login_crud.create_device_info(db,request,user.id)
            db.commit()
    
        except Exception as e:
            logger.error(str(e)) 
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid input data.")  
   
    # ユーザーのロールを取得
    role = login_crud.find_by_role(db, user.role_id)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return {
            "user_id": user.id,
            "access_token": access_token,
            "expires_in": 3600,
            "role": role.name
        }