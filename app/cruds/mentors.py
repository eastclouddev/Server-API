from sqlalchemy.orm import Session

from models.user_account_info import UserAccountInfo
from models.users import Users
from models.user_account_types import UserAccountTypes
from models.mentorships import Mentorships
from schemas.mentors import DetailResponseBody

def find_bank_info(db: Session, mentor_id: int):

    mentor_info = db.query(Mentorships).filter(Mentorships.mentor_id == mentor_id).first()

    if not mentor_info:
        return None
    
    bank_info = db.query(UserAccountInfo).filter(UserAccountInfo.user_id == mentor_info.mentor_id).first()
    if not bank_info:
        return None
    

    account_type = db.query(UserAccountTypes).filter(bank_info.user_id == UserAccountTypes.id).first()
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