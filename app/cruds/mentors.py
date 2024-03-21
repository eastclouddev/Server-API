from sqlalchemy.orm import Session
from schemas.mentors import ResponseBody
from models.user_account_info import UserAccountInfo
from models.user_account_types import UserAccountTypes
from models.users import Users
from fastapi import HTTPException

def create(db: Session, create_model: ResponseBody,mentor_id):

    mentor = db.query(Users).filter(Users.id == mentor_id).first()

    if not mentor:
        return None


    account_type_id = db.query(UserAccountTypes).filter(create_model.account_type == UserAccountTypes.name).first()


    new_transfer = UserAccountInfo(
        user_id = mentor_id,
        bank_name = create_model.bank_name,
        branch_name = create_model.branch_name,
        bank_code = create_model.bank_code,
        branch_code = create_model.branch_code,
        account_type_id = account_type_id.id,
        account_number = create_model.account_number,
        account_name = create_model.account_name
    
        )
    
    db.add(new_transfer)


    return new_transfer