from sqlalchemy.orm import Session

from schemas.companies import CompanyCreateRequestBody, CompanyUpdateRequestBody, \
CompanyBillingInfoCreateRequestBody, CompanyBillingInfoUpdateRequestBody
from models.companies import Companies 
from models.users import Users
from models.learning_statuses import LearningStatuses
from models.course_progresses import CourseProgresses
from models.sections import Sections
from models.curriculums import Curriculums
from models.roles import Roles
from models.users import Users
from models.company_billing_info import CompanyBillingInfo
from models.company_billing_statuses import CompanyBillingStatuses
from models.company_transaction_histories import CompanyTransactionHistories
from models.payment_methods import PaymentMethods
from models.courses import Courses

def create_company(db: Session, company_create: CompanyCreateRequestBody):
    new_company = Companies(**company_create.model_dump())
    db.add(new_company)
    return new_company

def update_company(db: Session, param: CompanyUpdateRequestBody, company_id: int):
    company = find_company_by_company_id(db, company_id)
    if not company:
        return None

    company.name = param.name
    company.name_kana = param.name_kana
    company.prefecture = param.prefecture
    company.city = param.city
    company.town = param.town
    company.address = param.address
    company.postal_code = param.postal_code
    company.phone_number = param.phone_number
    company.email = param.email
    db.add(company)

    return "success"

def find_company_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()

def find_companies(db: Session):
    return db.query(Companies).all()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_user_by_company_id(db: Session, company_id: int):
    return db.query(Users).filter(Users.company_id == company_id).all()

def find_progresses_by_user_id_list(db: Session, user_id_list: list):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id.in_(user_id_list)).all()

def find_user_by_user_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_section_by_course_id(db: Session, course_id: int):
    section = db.query(Sections).filter(Sections.course_id == course_id).first()
    if not section:
        return None
    return section.id

def find_curriculum_by_course_id(db: Session, course_id: int):
    section_id = find_section_by_course_id(db, course_id)
    if not section_id:
        return None
    curriculum = db.query(Curriculums).filter(Curriculums.section_id == section_id).first()
    if not curriculum:
        return None
    return curriculum.id

def find_status_by_status_id(db: Session, status_id: int):
    status = db.query(LearningStatuses).filter(LearningStatuses.id == status_id).first()
    if not status:
        return None
    return status.name

def find_users_by_company_id_and_role(db: Session, company_id: int, role: str):
    found_role = db.query(Roles).filter(Roles.name == role).first()
    if not found_role:
        return None
    users = db.query(Users).filter(Users.company_id == company_id, Users.role_id == found_role.id).all()
    return users

def find_role_by_role_id(db: Session, role_id: int):
    return db.query(Roles).filter(Roles.id == role_id).first()

def find_billing_by_company_id(db: Session, company_id: int):
    return db.query(CompanyBillingInfo).filter(CompanyBillingInfo.company_id == company_id).all()

def find_transaction_histories_by_billing_info_id(db: Session, billing_info_id_list: list):
    return db.query(CompanyTransactionHistories).filter(CompanyTransactionHistories.billing_info_id.in_(billing_info_id_list)).all()

def find_billing_status_by_status_id(db: Session, status_id: int):
    return db.query(CompanyBillingStatuses).filter(CompanyBillingStatuses.id == status_id).first()

def find_users_by_company_id(db: Session, company_id: int):
    return db.query(Users).filter(Users.company_id == company_id).first()

def find_roles(db: Session):
    return db.query(Roles).all()

def find_users_by_role_id(db: Session, role_id: int):
    return db.query(Users).filter(Users.role_id == role_id, Users.is_enable == True).all()

def create_company_billing_info(db: Session, company_billing_info_create: CompanyBillingInfoCreateRequestBody):
    new_company_billing_info = CompanyBillingInfo(**company_billing_info_create.model_dump())
    
    company_billing_info = {
        "company_billing_info_id": new_company_billing_info.id,
        "prefecture": new_company_billing_info.prefecture,
        "city": new_company_billing_info.city,
        "town": new_company_billing_info.town,
        "address": new_company_billing_info.address,
        "postal_code": new_company_billing_info.postal_code,
        "phone_number": new_company_billing_info.phone_number,
        "billing_email": new_company_billing_info.billing_email,
        "invoice_number": new_company_billing_info.invoice_number,
        "tax_number": new_company_billing_info.tax_number,
        "notes": new_company_billing_info.notes,
        "last_receipt_number": new_company_billing_info.last_receipt_number,
        "created_at": new_company_billing_info.created_at.isoformat()
    }
    db.add(company_billing_info)
    return company_billing_info

def find_company_billing_info_by_billing_info_id(db: Session, billing_info_id: int):
    company_billing_info = db.query(CompanyBillingInfo).filter(CompanyBillingInfo.id == billing_info_id).first()
    # 現状不要
    # payment_method = db.query(PaymentMethods).filter(PaymentMethods.id == company_billing_info.payment_method_id).first()
    di = {
        "company_billing_info_id": billing_info_id,
        "prefecture": company_billing_info.prefecture,
        "city": company_billing_info.city,
        "town": company_billing_info.town,
        "address": company_billing_info.address,
        "postal_code": company_billing_info.postal_code,
        "phone_number": company_billing_info.phone_number,
        "billing_email": company_billing_info.billing_email,
        "invoice_number": company_billing_info.invoice_number,
        "tax_number": company_billing_info.tax_number,
        "notes": company_billing_info.notes,
        "last_receipt_number": company_billing_info.last_receipt_number,
        "created_at": company_billing_info.created_at.isoformat(),
        "updated_at": company_billing_info.updated_at.isoformat()
    }
    return di

def update_company_billing_info(db: Session, update:CompanyBillingInfoUpdateRequestBody ,billing_info_id: int):
    company_billing_info = find_company_billing_info_by_billing_info_id(db, billing_info_id)
    if not company_billing_info:
        return None
    
    company_billing_info.content = update.content
    company_billing_info.is_read = update.is_read
    db.add(company_billing_info)
    
    update_company_billing_info = {
        "company_billing_info_id": billing_info_id,
        "prefecture": company_billing_info.prefecture,
        "city": company_billing_info.city,
        "town": company_billing_info.town,
        "address": company_billing_info.address,
        "postal_code": company_billing_info.postal_code,
        "phone_number": company_billing_info.phone_number,
        "billing_email": company_billing_info.billing_email,
        "invoice_number": company_billing_info.invoice_number,
        "tax_number": company_billing_info.tax_number,
        "notes": company_billing_info.notes,
        "last_receipt_number": company_billing_info.last_receipt_number,
        "updated_at": company_billing_info.updated_at.isoformat() 
    }

    return update_company_billing_info