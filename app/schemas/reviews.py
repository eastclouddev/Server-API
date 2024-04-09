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

class AllResponseList(BaseModel):
    id: int 
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool

class AllResponseBody(BaseModel):
    reviews: list[AllResponseList]

class ReviewRequestBody(BaseModel):
    id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    is_closed: bool
    created_at: str
    updated_at: str

class ReviewResponseBody(BaseModel):
    id: int
    review_request_id: int
    user_id: int
    parent_response_id: Optional[int]
    content: str
    is_read: bool
    created_at: str

class AllReviewResponse(BaseModel):
    review_request: ReviewRequestBody
    responses: list[ReviewResponseBody]