from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class CurriculumProgresses(Base):
    __tablename__ = "curriculum_progresses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    status_id = Column(Integer, ForeignKey("learning_statuses.id"), nullable=False, default=0)
    started_at = Column(DateTime, default=None)
    last_accessed_at = Column(DateTime, default=None)
    completed_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
