from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class BoardInvoices(Base):
    __tablename__ = "board_invoices"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    invoice_id = Column(Integer)
    project_id = Column(Integer)
    client_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
