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
    thumbnail_url: str
    created_at: str

class AllResponseBody(BaseModel):
    courses: list[Course]

class CurriculumList(BaseModel):
    curriculum_id: int
    title: str
    description: str

class SectionList(BaseModel):
    section_id: int
    title: str
    description: str
    curriculums: list[CurriculumList]

class DetailResponseBody(BaseModel):
    course_id: int
    title: str
    description: str
    created_user_id: int
    created_at: str
    sections: list[SectionList]