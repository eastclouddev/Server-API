from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CurriculumList(BaseModel):
    curriculum_id: int
    title: str
    description: str

class SectionList(BaseModel):
    section_id: int
    title: str
    description: str
    curriculums: list[CurriculumList]

class ResponseBody(BaseModel):
    course_id: int
    title: str
    description: str
    created_user_id: int
    created_at: str
    sections: list[SectionList]