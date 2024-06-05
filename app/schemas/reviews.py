from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    user_id: int
    name: str

class ReviewResponseCreateRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    parent_response_id: Optional[int] = Field(examples=[1])
    content: str = Field(examples=["回答の内容"])
    media_content: Optional[list] = Field(None, examples=[[{"url": "aaa.com"}, {"url": "bbb.com"}]])

class ReviewResponseCreateResponseBody(BaseModel):
    id: int
    review_request_id: int
    user: User
    parent_response_id: Optional[int]
    content: str
    media_content: Optional[list]
    created_at: str

class ReviewResponseUpdateRequestBody(BaseModel):
    content: Optional[str] = Field(examples=["content"])
    is_read: Optional[bool] = Field(examples=[False])

class ReviewResponseUpdateResponseBody(BaseModel):
    id: int
    review_request_id: int
    user_id: int
    parent_response_id: Optional[int]
    content: str
    is_read: bool
    updated_at: str

class ReviewRequestUpdateRequestBody(BaseModel):
    title: Optional[str] = Field(examples=["title"])
    content: Optional[str] = Field(examples=["content"])
    is_closed: Optional[bool] = Field(examples=[False])

class ReviewRequestUpdateResponseBody(BaseModel):
    id: int
    title: str
    content: str
    is_closed: bool
    updated_at: str

class ReviewRequestBody(BaseModel):
    id: int
    curriculum_id: int
    user: User
    title: str
    content: str
    media_content: Optional[list]
    is_closed: bool
    created_at: str

class ReviewResponseBody(BaseModel):
    id: int
    review_request_id: int
    user: User
    parent_response_id: Optional[int]
    content: str
    media_content: Optional[list]
    created_at: str

class ReviewThreadDetailResponseBody(BaseModel):
    review_request: ReviewRequestBody
    review_responses: list[ReviewResponseBody]