from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.course_progresses import CourseProgresses
from models.curriculum_progresses import CurriculumProgresses
from models.section_progresses import SectionProgresses

class LearningStatuses(Base):
    __tablename__ = "learning_statuses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    course_progresses = relationship("CourseProgresses", backref="learning_statuses")
    curriculum_progresses = relationship("CurriculumProgresses", backref="learning_statuses")
    section_progresses = relationship("SectionProgresses", backref="learning_statuses")
