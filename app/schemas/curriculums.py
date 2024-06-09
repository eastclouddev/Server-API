from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    user_id: int
    name: str

class CurriculumDetailResponseBody(BaseModel):
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

class ReviewRequestListResponseBody(BaseModel):
    reviews: list[Review]

class ReviewRequestCreateResponseBody(BaseModel):
    id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    is_closed: bool
    created_at: str

class ReviewRequestCreateRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    title: str = Field(examples=["Reviewのタイトル"])
    content: str = Field(examples=["Reviewの内容"])
    is_closed: bool = Field(examples=[False])

class MediaContent(BaseModel):
    url: str

class QuestionCreateRequestBody(BaseModel):
    curriculum_id : int = Field(examples=[1])
    user_id: int = Field(examples=[1])
    title: str = Field(examples=["title"])
    objective: str = Field(examples=["やりたいこと"])
    current_situation: str = Field(examples=["現状"])
    research: str = Field(examples=["調べたこと"])
    content: str = Field(examples=["質問内容"])
    media_content: list[MediaContent]

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

class QuestionList(BaseModel):
    question_id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    media_content: list[MediaContent]

class QuestionListResponseBody(BaseModel):
    questions: list[QuestionList]

