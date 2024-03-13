from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.company_billing_info import CompanyBillingInfo
from models.company_receipts import CompanyReceipts
from models.users import Users

class Companies(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    prefecture = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    town = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    postal_code = Column(String(10), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    company_billing_info = relationship("CompanyBillingInfo", backref="companies")
    company_receipts = relationship("CompanyReceipts", backref="companies")
    users = relationship("Users", backref="companies")
