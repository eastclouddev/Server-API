from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

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

class NotificationUpdateResponseBody(BaseModel):
    message: str
    notification_id: int