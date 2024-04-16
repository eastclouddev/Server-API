from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.curriculum_progresses import CurriculumProgresses
from models.questions import Questions
from models.quiz_contents import QuizContents
from models.review_requests import ReviewRequests

class Curriculums(Base):
    __tablename__ = "curriculums"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    content = Column(Text)
    display_no = Column(Integer, nullable=False)
    video_url = Column(String(255))
    is_test = Column(Boolean, default=False)
    media_content = Column(JSON)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    curriculum_progresses = relationship("CurriculumProgresses", backref="curriculums")
    questions = relationship("Questions", backref="curriculums")
    quiz_contents = relationship("QuizContents", backref="curriculums")
    review_requests = relationship("ReviewRequests", backref="curriculums")

