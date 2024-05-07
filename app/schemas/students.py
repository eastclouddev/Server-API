from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass

class Questions(BaseModel):
    id: int
    title: str
    content: str
    curriculum_id: int
    created_at: datetime
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
    created_at: str
    is_read: bool
    is_closed: bool

class AllResponseBody(BaseModel):
    reviews: list[ReviewResponse]

class NotificationsResponse(BaseModel):
    id: int 
    from_user_id: int
    from_user_name: str
    content: str
    related_question_id: Optional[int]
    related_answer_id: Optional[int]
    related_review_request_id: Optional[int]
    related_review_response_id: Optional[int]
    is_read: bool
    created_at: str

class NotificationListResponseBody(BaseModel):
    notifications: list[NotificationsResponse]

class ReviewRequestListResponseBody(BaseModel):
    reviews: list[ReviewResponse]
