from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class DetailResponseBody(BaseModel):
    curriculum_id: int
    title: str
    description: str
    video_url: Optional[str] = None
    content: Optional[str] = None
    is_test: bool
    display_no: int

class Review(BaseModel):
    id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    is_closed: bool
    created_at: str
    updated_at: str

class ReviewsResponseBody(BaseModel):
    reviews: list[Review]

class ReviewResponse(BaseModel):
    id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    is_closed: bool
    created_at: str

class ReviewRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    title: str = Field(examples=["Reviewのタイトル"])
    content: str = Field(examples=["Reviewの内容"])
    is_closed: bool = Field(examples=[False])

class MediaContent(BaseModel):
    url: str

class RequestBody(BaseModel):
    user_id: int
    title: str
    content: str
    media_content: MediaContent

class ResponseBody(BaseModel):
    question_id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    media_content: list
