from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class CompanyTransactionHistories(Base):
    __tablename__ = "company_transaction_histories"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    billing_info_id = Column(Integer, ForeignKey("company_billing_info.id"), nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    billing_status_id = Column(Integer, ForeignKey("company_billing_statuses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
