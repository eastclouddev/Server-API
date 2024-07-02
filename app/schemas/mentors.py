from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProgressesResponseList(BaseModel):
    user_id: int
    user_name: str
    course_id: int
    course_name: str
    section_id: Optional[int]
    curriculum_id: Optional[int]
    progress_percentage: int
    status: str

class ProgressListResponseBody(BaseModel):
    progresses: list[ProgressesResponseList]

class Question(BaseModel):
    id: int
    title: str
    objective: str
    current_situation: str
    research: str
    content: str
    curriculum_id: int
    tech_category: str
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
    tech_category: str
    created_at: str
    is_read: bool
    number_of_comments: int
    is_closed: bool

class ReviewRequestListResponseBody(BaseModel):
    reviews: list[AllResponseList]

class MentorsCountList(BaseModel):
    mentor_id: int
    mentor_name: str
    student_count: int

class MentorsCountListResponseBody(BaseModel):
    mentors: list[MentorsCountList]

class User(BaseModel):
    id: int
    name: str
class Notification(BaseModel):
    id: int
    from_user: User
    question_id: Optional[int]
    answer_id: Optional[int]
    review_request_id: Optional[int]
    review_response_id: Optional[int]
    title: str
    content: str
    is_read: bool
    created_at: str

class NotificationListResponseBody(BaseModel):
    notifications: list[Notification]