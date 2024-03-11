from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class UserRewards(Base):
    __tablename__ = "user_rewards"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    reason = Column(String(255))
    reward_at = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
