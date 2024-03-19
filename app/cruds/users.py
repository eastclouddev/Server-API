from sqlalchemy.orm import Session
from models.users import Users
from schemas.users import UserUpdate
from logging import getLogger

from models.companies import Companies
from models.roles import Roles

logger = getLogger("uvicorn.app")

def find_by_id(db: Session, id: str):
    return db.query(Users).filter(Users.id == id).first()

def find_by_email(db: Session, email: str, user_id: int):
    user = db.query(Users).filter(Users.email == email).first()

    # 重複しているユーザーがいない or 更新対象と同じメールアドレス
    if not user or (user.id == user_id):
        return None
    else:
        return user

def update_by_user(db: Session, param:UserUpdate, user_id: str):
    # 更新対象のユーザーを取得
    user = find_by_id(db, user_id)
    if not user:
        return None
    
    # 更新
    user.first_name = param.first_name
    user.last_name = param.last_name
    user.first_name_kana = param.first_name_kana
    user.last_name_kana = param.last_name_kana
    user.email = param.email
    db.add(user)
    return user
