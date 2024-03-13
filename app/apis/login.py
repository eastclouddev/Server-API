from fastapi import HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from logging import getLogger
from typing import Annotated
from database.database import get_db
from schemas.login import RequestBody
from cruds import login as login_crud
from services import login as login_service
import hashlib

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/login", tags=["Login"])


# ログインエンドポイント
# 与えられたメールアドレスとパスワードでユーザーを認証し、
# 認証が成功した場合は、アクセストークンを生成
# 認証が失敗した場合は、HTTPExceptionを返す
@router.post("")
async def login(db: DbDependency, request: RequestBody):
    """
    ログイン認証
    
    Parameters
    ----------
    request: RequestBody
        email
        password
        device_info: device_type
                     device_name
                     uuid
                    
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
   
    # ログインした際の情報を返す
    role = login_crud.find_by_role(db, user.role_id)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    else:
        return {
            "user_id":user.id,
            "access_token":access_token,
            "expires_in":3600,
            "role":role.name
    }


