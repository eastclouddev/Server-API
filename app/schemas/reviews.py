from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UpdateResponseRequestBody(BaseModel):
    content: Optional[str] = Field(examples=["content"])
    is_read: Optional[bool] = Field(examples=[False])

class UpdateResponseResponseBody(BaseModel):
    id: int
    review_request_id: int
    user_id: int
    parent_response_id: Optional[int]
    content: str
    is_read: bool
    updated_at: str

class UpdateReviewRequestBody(BaseModel):
    title: Optional[str] = Field(examples=["title"])
    content: Optional[str] = Field(examples=["content"])
    is_closed: Optional[bool] = Field(examples=[False])

class UpdateReviewResponseBody(BaseModel):
    id: int
    title: str
    content: str
    is_closed: bool
    updated_at: str