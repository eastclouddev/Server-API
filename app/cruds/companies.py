from sqlalchemy.orm import Session
from schemas.companies import CompanyUpdate
from models.companies import Companies 


def find_all(db: Session):
    return db.query(Companies).all()

def find_by_id(db: Session, id: int):
    return db.query(Companies).filter(Companies.id == id).first()

def update(db: Session, id: int, company_update: CompanyUpdate):

    company = find_by_id(db, id)
    
    if company:
        update_data = company_update.model_dump()
        for key, value in update_data.items():
            setattr(company, key, value)

        db.add(company)
        db.commit()
        db.refresh(company)

    return company