from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, Numeric, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class SectionTags(Base):
    __tablename__ = "section_tags"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
