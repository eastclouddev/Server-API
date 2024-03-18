from sqlalchemy.orm import Session
from schemas.users import UserCreate
from models.users import Users
from models.companies import Companies
from models.roles import Roles


def create(db: Session, user_create: UserCreate):
    new_user = Users(**user_create.model_dump())
    db.add(new_user)
    return new_user