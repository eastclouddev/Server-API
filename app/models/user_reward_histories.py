from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class UserRewardHistories(Base):
    __tablename__ = "user_reward_histories"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    target_year_month = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
