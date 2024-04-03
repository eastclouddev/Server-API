from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class Course(BaseModel):
    course_id: int
    title: str
    description: str
    created_user: int
    thumbnail_url: Optional[str]
    created_at: str

class AllResponseBody(BaseModel):
    courses: list[Course]

class Curriculum(BaseModel):
    curriculum_id: int
    title: str
    description: Optional[str]

class Section(BaseModel):
    section_id: int
    title: str
    description: Optional[str]
    curriculums: list[Curriculum]

class DetailResponseBody(BaseModel):
    course_id: int
    title: str
    description: str
    created_user_id: int
    created_at: str
    sections: list[Section]