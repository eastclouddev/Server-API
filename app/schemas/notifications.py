from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

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

class ListResponseBody(BaseModel):
    notifications: list[NotificationsResponse]