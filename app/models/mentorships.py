from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from database.database import Base

from models.answers import Answers

class Mentorships(Base):
    __tablename__ = "mentorships"
    __table_args__ = (
        ForeignKeyConstraint(
            ["mentor_id", "student_id"],
            ["users.id", "users.id"],
        ),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    mentor_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())