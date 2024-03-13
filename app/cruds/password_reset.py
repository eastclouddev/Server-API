import hashlib

from sqlalchemy.orm import Session
from models.users import Users
from logging import getLogger

logger = getLogger("uvicorn.app")

def find_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


def update_by_password(db: Session, email: str, new_password: str):
    # 該当のユーザーを取得
    user = find_by_email(db, email)
    if not user:
        return None

    # 新しいパスワードを暗号化して登録
    user.password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
    db.add(user)
    return user
