from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    user_id: int
    name: str

class MediaContent(BaseModel):
    url: str

class ReviewRequestCreateRequestBody(BaseModel):
    curriculum_id: int = Field(examples=[1])
    user_id: int = Field(examples=[1])
    title: str = Field(examples=["Reviewのタイトル"])
    content: str = Field(examples=["Reviewの内容"])
    media_content: list[MediaContent]

class ReviewRequestCreateResponseBody(BaseModel):
    id: int
    curriculum_id: int
    user: User
    title: str
    content: str
    media_content: list[MediaContent]
    created_at: str
    is_read: bool
    is_closed: bool
    reply_counts: int

class ReviewRequest(BaseModel):
    id: int
    user: User
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool
    reply_counts: int

class ReviewRequestListResponseBody(BaseModel):
    reviews: list[ReviewRequest]

class QuestionCreateResponseBody(BaseModel):
    question_id: int
    curriculum_id: int
    user: User
    title: str
    objective: str
    current_situation: str
    research: str
    content: str
    media_content: list[MediaContent]
    created_at: str
    is_read: bool
    is_closed: bool
    reply_counts: int

class QuestionCreateRequestBody(BaseModel):
    curriculum_id : int = Field(examples=[1])
    user_id: int = Field(examples=[1])
    title: str = Field(examples=["title"])
    objective: str = Field(examples=["やりたいこと"])
    current_situation: str = Field(examples=["現状"])
    research: str = Field(examples=["調べたこと"])
    content: str = Field(examples=["質問内容"])
    media_content: list[MediaContent]

class QuestionList(BaseModel):
    question_id: int
    user: User
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool
    reply_counts: int

class QuestionListResponseBody(BaseModel):
    questions: list[QuestionList]


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
    duration: str
    is_completed: bool

class Section(BaseModel):
    section_id: int
    title: str
    description: Optional[str]
    duration: str
    curriculums: list[Curriculum]

class CourseDetailResponseBody(BaseModel):
    course_id: int
    title: str
    description: str
    created_user_id: int
    thumbnail_url: Optional[str]
    expected_end_hours: int
    total_curriculums: int
    tech_category: str
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