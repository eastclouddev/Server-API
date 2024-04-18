from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class TestContents(Base):
    __tablename__ = "test_contents"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"), nullable=False)
    question = Column(Text, nullable=False)
    media_content = Column(JSON)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
