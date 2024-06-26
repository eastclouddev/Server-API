from sqlalchemy.orm import Session

from schemas.users import UpdateRequestBody
from models.users import Users
from models.companies import Companies
from models.roles import Roles



def find_by_user_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_by_role_id(db: Session, role_id: int):
    return db.query(Roles).filter(Roles.id == role_id).first()

def find_by_email(db: Session, email: str, user_id: int):
    user = db.query(Users).filter(Users.email == email).first()

    # 重複しているユーザーがいない or 更新対象と同じメールアドレス
    if not user or (user.id == user_id):
        return None
    else:
        return user

def update_user(db: Session, param:UpdateRequestBody, user_id: str):
    # 更新対象のユーザーを取得
    user = find_by_user_id(db, user_id)
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

def find_user(db:Session,user_id:int):
    return db.query(Users).filter(Users.id == user_id).first()

def update_address(db,found_user,token_info):
    found_user.email = token_info["email"]

    db.add(found_user)
    return found_user