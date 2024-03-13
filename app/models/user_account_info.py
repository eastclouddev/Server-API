from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class UserAccountInfo(Base):
    __tablename__ = "user_account_info"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_name = Column(String(255), nullable=False)
    bank_code = Column(String(10), nullable=False)
    branch_name = Column(String(255))
    branch_code = Column(String(10))
    account_type_id = Column(Integer, ForeignKey("user_account_types.id"), nullable=False)
    account_number = Column(String(255), nullable=False)
    account_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
