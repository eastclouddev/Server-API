from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from models.curriculums import Curriculums
from models.section_progresses import SectionProgresses


class Sections(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    display_no = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    curriculums = relationship("Curriculums", backref="sections")
    section_progresses = relationship("SectionProgresses", backref="sections")
