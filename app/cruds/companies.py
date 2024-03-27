from sqlalchemy.orm import Session

from schemas.companies import CreateRequestBody
from models.companies import Companies 


def create_company(db: Session, company_create: CreateRequestBody):
    new_company = Companies(**company_create.model_dump())
    db.add(new_company)
    return new_company

def find_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_companies(db:Session):
    return db.query(Companies).all()