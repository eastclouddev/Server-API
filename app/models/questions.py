from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.answers import Answers

class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    media_content = Column(JSON)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    answers = relationship("Answers", backref="questions")