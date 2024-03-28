from sqlalchemy.orm import Session

from schemas.mentors import CreateResponseBody
from models.user_account_info import UserAccountInfo
from models.users import Users
from models.user_account_types import UserAccountTypes
from models.mentorships import Mentorships
from models.user_rewards import UserRewards 


def find_rewards_by_mentor_id(db: Session, mentor_id: int):
    return db.query(UserRewards).filter(UserRewards.user_id == mentor_id).all()

def find_bank_info(db: Session, mentor_id: int):

    mentor_info = db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).first()

    if not mentor_info:
        return None

    bank_info = db.query(UserAccountInfo).filter(UserAccountInfo.user_id == mentor_info.mentor_id).first()
    if not bank_info:
        return None

    account_type = db.query(UserAccountTypes).filter(UserAccountTypes.id == bank_info.user_id).first()
    if not account_type:
        return None

    #請求履歴詳細
    info = {
        "mentor_id":  mentor_id,
        "account_name": bank_info.account_name,
        "bank_name": bank_info.bank_name,
        "branch_name": bank_info.branch_name,
        "account_number": bank_info.account_number,
        "account_type": account_type.name 
    }

    return info

def create(db: Session, create_model: CreateResponseBody, mentor_id: int):

    mentor = db.query(Users).filter(Users.id == mentor_id).first()

    if not mentor:
        return None

    account_type = db.query(UserAccountTypes).filter(UserAccountTypes.name == create_model.account_type).first()

    if not account_type:
        return None

    new_transfer = UserAccountInfo(
        user_id = mentor_id,
        bank_name = create_model.bank_name,
        branch_name = create_model.branch_name,
        bank_code = create_model.bank_code,
        branch_code = create_model.branch_code,
        account_type_id = account_type.id,
        account_number = create_model.account_number,
        account_name = create_model.account_name
    )
    
    db.add(new_transfer)

    return new_transfer