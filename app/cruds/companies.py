from sqlalchemy.orm import Session
from schemas.companies import RequestBody
from models.companies import Companies 


def create(db: Session, company_create: RequestBody):
    new_company = Companies(**company_create.model_dump())
    db.add(new_company)
    return new_company

