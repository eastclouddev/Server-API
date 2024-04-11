from sqlalchemy.orm import Session

from schemas.companies import CreateRequestBody
from models.companies import Companies
from models.roles import Roles
from models.users import Users


def create_company(db: Session, company_create: CreateRequestBody):
    new_company = Companies(**company_create.model_dump())
    db.add(new_company)
    return new_company

def find_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_companies(db:Session):
    return db.query(Companies).all()

def get_user(db: Session, company_id:int,role:str):
    found_role = db.query(Roles).filter(Roles.name == role).first()
    users = db.query(Users).filter(Users.company_id == company_id ,Users.role_id == found_role.id).all()
    return users