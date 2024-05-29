from sqlalchemy.orm import Session

from schemas.users import UserCreateRequestBody, UserUpdateRequestBody
from models.users import Users
from models.companies import Companies
from models.roles import Roles


def create_user(db: Session, param: UserCreateRequestBody):
    new_user = Users(
        company_id = 1,
        first_name = param.first_name,
        last_name = param.last_name,
        first_name_kana = param.first_name_kana,
        last_name_kana = param.last_name_kana,
        password = "adbeljldk",
        email = param.email,
        role_id = 1,
    )
    db.add(new_user)
    return new_user

def find_user_by_user_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_role_by_role_id(db: Session, role_id: int):
    return db.query(Roles).filter(Roles.id == role_id).first()

def find_company_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()

def update_user(db: Session, param: UserUpdateRequestBody, user_id: str):
    # 更新対象のユーザーを取得
    user = find_user_by_user_id(db, user_id)
    if not user:
        return None
    
    # 更新
    user.first_name = param.first_name
    user.last_name = param.last_name
    user.first_name_kana = param.first_name_kana
    user.last_name_kana = param.last_name_kana
    user.email = param.email
    user.is_enable = param.is_enable
    db.add(user)
    return user

def update_email(db: Session, found_user, token_info):
    found_user.email = token_info["email"]

    db.add(found_user)
    return found_user

def find_users_by_role(db: Session, role: str):
    find_role = db.query(Roles).filter(Roles.name == role).first()
    if not find_role:
        return []
    users = db.query(Users).filter(Users.role_id == find_role.id).all()
    return users

def find_roles(db: Session):
    return db.query(Roles).all()

def find_users_by_role_id(db: Session, role_id: int):
    return db.query(Users).filter(Users.role_id == role_id, Users.is_enable == True).all()