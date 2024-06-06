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
    expected_end_hours: int
    total_curriculums: int
    tech_category: str
    created_at: str

class CourseListResponseBody(BaseModel):
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

class CourseDetailResponseBody(BaseModel):
    course_id: int
    title: str
    description: str
    created_user_id: int
    created_at: str
    sections: list[Section]

class CoursesStartRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    course_ids: list[int] = Field(examples=[[1, 2, 3]])

class CourseStart(BaseModel):
    course_id: int
    started_at: str
class CoursesStartResponsetBody(BaseModel):
    courses: list[CourseStart]