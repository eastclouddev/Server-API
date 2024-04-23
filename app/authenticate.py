import hashlib
from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from models.users import Users
from models.access_token import AccessToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO:専用のファイルから取得する
SECRET_KEY = "SECRET_KEY123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 10

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    token_type: Union[str, None] = None
    user_id: Union[int, None] = None

class UserInDB(BaseModel):
    user_id: int
    hashed_password: str


# emailを条件にユーザーを取得
def find_user_by_email(db: Session, username: str):
    found_user = db.query(Users).filter(Users.email == username).first()
    if not found_user:
        return None
    user_info = {
        "user_id": found_user.id,
        "hashed_password": found_user.password
    }
    return UserInDB(**user_info)

# idを条件にユーザーを取得
def find_user_by_id(db: Session, user_id: int):
    found_user = db.query(Users).filter(Users.id == user_id).first()
    if not found_user:
        return None
    user_info = {
        "user_id": found_user.id,
        "hashed_password": found_user.password
    }
    return UserInDB(**user_info)
    
# ユーザーの認証
def authenticate_user(db: Session, username: str, password: str):
    user = find_user_by_email(db, username)
    if not user:
        return False
    if hashlib.sha256(password.encode("utf-8")).hexdigest() != user.hashed_password:
        return False
    return user

# アクセストークン生成
def create_access_token(user_id):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "token_type": "access_token",
        "exp": expire,
        "user_id": user_id
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# リフレッシュトークン生成
def create_refresh_token(db: Session, user_id):
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "token_type": "refresh_token",
        "exp": expire,
        "user_id": user_id
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # リフレッシュトークンをDBに保存
    refresh_token = db.query(AccessToken).filter(AccessToken.user_id == user_id).first()
    try:
        if refresh_token:
            refresh_token.token = encoded_jwt
            refresh_token.expires_at = expire
        else:
            token_info = {
                "user_id": user_id,
                "token": encoded_jwt,
                "expires_at": expire
            }
            refresh_token = AccessToken(**token_info)
        db.add(refresh_token)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="")
    return encoded_jwt

# アクセストークンよりユーザー情報を取得
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    token_data = {
        "token_type": payload.get("token_type"),
        "user_id": user_id
    }
    return TokenData(**token_data)