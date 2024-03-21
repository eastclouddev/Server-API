from sqlalchemy.orm import Session
from models.companies import Companies 


def find_by_detail(db: Session, company_id: int):
    company_info = db.query(Companies).filter(Companies.id == company_id).first()
    if not company_info:
        return None
    


    info = {
        "company_id": company_id,
        "name": company_info.name,
        "prefecture": company_info.prefecture,
        "city": company_info.city,
        "town": company_info.town,
        "address": company_info.address,
        "postal_code": company_info.postal_code,
        "phone_number": company_info.phone_number,
        "email": company_info.email,
        "created_at": company_info.created_at,
        "updated_at": company_info.updated_at
    }



    return info