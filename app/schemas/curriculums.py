from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

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

class Quizzes(BaseModel):
    test_id: int
    question: str
    options: list[str]
    correct_answer: str
    explanation: str
    media_content_url: list[str]

class QuizDetailResponseBody(BaseModel):
    curriculum_id: int
    tests: list[Quizzes]

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
    user_id: int = Field(default=1)
    title: str
    content: str
    media_content: list[MediaContent]

class QuestionCreateResponseBody(BaseModel):
    question_id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    media_content: list[MediaContent]

class QuestionListResponseBody(BaseModel):
    questions: list[QuestionCreateResponseBody]

