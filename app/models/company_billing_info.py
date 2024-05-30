from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.company_receipts import CompanyReceipts
from models.company_transaction_histories import CompanyTransactionHistories

class CompanyBillingInfo(Base):
    __tablename__ = "company_billing_info"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    prefecture = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    town = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    invoice_number = Column(String(255), nullable=False)
    tax_number = Column(String(255), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    notes = Column(Text)
    last_receipt_number = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    company_receipts = relationship("CompanyReceipts", backref="company_billing_info")
    company_transaction_histories = relationship("CompanyTransactionHistories", backref="company_billing_info")
