from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProgressesResponseList(BaseModel):
    progress_id: int
    user_id: int
    course_id: int
    section_id: Optional[int]
    curriculum_id: Optional[int]
    progress_percentage: int
    status: str

class ProgressListResponseBody(BaseModel):
    progresses: list[ProgressesResponseList]

class Question(BaseModel):
    id: int
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool

class QuestionListResponseBody(BaseModel):
    questions: list[Question]

class AllResponseList(BaseModel):
    id: int 
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool

class ReviewRequestListResponseBody(BaseModel):
    reviews: list[AllResponseList]

class MentorsCountList(BaseModel):
    mentor_id: int
    mentor_name: str
    student_count: int

class MentorsCountListResponseBody(BaseModel):
    mentors: list[MentorsCountList]
