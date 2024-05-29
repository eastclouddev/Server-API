from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.course_progresses import CourseProgresses
from models.learning_records import LearningRecords
from models.section_tags import SectionTags
from models.sections import Sections


class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    thumbnail_url = Column(String(255), nullable=False)
    skill_level_id = Column(Integer, ForeignKey("skill_levels.id"), nullable=False)
    expected_end_hours = Column(Integer, nullable=False)
    tech_category_id = Column(Integer, ForeignKey("tech_categories.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    course_progresses = relationship("CourseProgresses", backref="courses")
    learning_records = relationship("LearningRecords", backref="courses")
    section_tags = relationship("SectionTags", backref="courses")
    sections = relationship("Sections", backref="courses")
