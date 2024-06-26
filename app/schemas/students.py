from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass

class Questions(BaseModel):
    id: int
    title: str
    objective: str
    current_situation: str
    research: str
    content: str
    curriculum_id: int
    created_at: datetime
    tech_category: str
    is_read: bool
    is_closed: bool
      
class QuestionListResponseBody(BaseModel):
    questions: list[Questions]

class Progress(BaseModel):
    course_id: int
    course_title: str
    progress_percentage: int
    status: str
    last_accessed_at: str

class ProgressListResponseBody(BaseModel):
    progresses: list[Progress]

class ReviewResponse(BaseModel):
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
    reviews: list[ReviewResponse]

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