from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_answer_id = Column(Integer, ForeignKey("answers.id"), default=None)
    content = Column(Text, nullable=False)
    media_content = Column(JSON)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
