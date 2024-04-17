import hashlib
from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

from sqlalchemy.orm import Session
from database.database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from models.users import Users
from models.access_token import AccessToken

DbDependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 　TODO:いずれimportで紐づける
SECRET_KEY = "SECRET_KEY123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
    id: int

# 指定された平文パスワードがハッシュ化されたパスワードと一致するかどうかを確認
def verify_password(plain_password, hashed_password):
    hashed_plain_password = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return hashed_plain_password == hashed_password

# 画面から受け取るemailからデータベースから指定されたユーザー名のユーザー情報を取得
def get_user_email(db: Session, username: str):                 # usernameにはemailが入っている
    found_user = db.query(Users).filter(Users.email == username).first()
    if not found_user:
        return None
    user_info = {
        "hashed_password":found_user.password,
        "user_id":found_user.id
    }
    return user_info
# トークンのuser_idからデータベースから指定されたユーザー名のユーザー情報を取得
def get_user_id(db: Session, user_id: int):
    found_user = db.query(Users).filter(Users.id == user_id).first()
    if not found_user:
        return None
    user_info = {
        "hashed_password":found_user.password,
        "user_id":found_user.id
    }
    return user_info
    
# ユーザーの認証
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_email(db, username)
    if not user:
        return False
    # 平文パスワードがハッシュ化されたパスワードと一致するかどうかを確認
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# アクセストークンを生成
def create_access_token(db:Session, data: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "token_type": "access_token",
        "exp": expire,
        "user_id": data["user_id"]
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# リフレッシュトークンを生成
def create_refresh_token(db:Session, data: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "token_type": "refresh_token",
        "exp": expire,
        "user_id": data["user_id"]
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # リフレッシュトークンをDBに保存
    access_token = db.query(AccessToken).filter(AccessToken.user_id == data["user_id"]).first()
    try:
        if access_token:
            access_token.token = encoded_jwt
            db.add(access_token)
            db.commit()
        else:
            token_info = {
            "user_id": data["user_id"],
            "token": encoded_jwt,
            "expires_at": expire
            }
            create_token = AccessToken(**token_info)
            db.add(create_token)
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
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload, token