from sqlalchemy.orm import Session

from models.company_receipts import CompanyReceipts
from models.companies import Companies
from models.payment_methods import PaymentMethods


def find_by_receipt_id(db: Session, receipt_id: int):
    return db.query(CompanyReceipts).filter(CompanyReceipts.id == receipt_id).first()


def find_by_company_id(db: Session, company_id: int):
    return db.query(Companies).filter(Companies.id == company_id).first()


def find_by_payment_method_id(db: Session, payment_method_id: int):
    return db.query(PaymentMethods).filter(PaymentMethods.id == payment_method_id).first()