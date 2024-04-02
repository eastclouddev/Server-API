from sqlalchemy.orm import Session

from models.users import Users
from models.companies import Companies
from models.roles import Roles

def find_user(db:Session,user_id:int):
    return db.query(Users).filter(Users.id == user_id).first()

def update_address(db,found_user,token_info):
    found_user.email = token_info["email"]

    db.add(found_user)
    return found_user