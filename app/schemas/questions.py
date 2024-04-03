from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    content: str = Field(examples=["内容を記載"])

class CreateResponseBody(BaseModel):
    answer_id: int
    question_id: int
    user_id: int
    content: str

class ResponseQuestion(BaseModel):
    id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    media_content: dict
    is_closed: bool
    created_at: str

class ResponseList(BaseModel):
    id: int
    question_id: int
    user_id: int
    parent_answer_id: Optional[int]
    content: str
    media_content: Optional[dict]
    is_read: bool
    created_at: str

class DetailResponseBody(BaseModel):
    question: ResponseQuestion
    answer: list[ResponseListfrom typing import Optional
from pydantic import BaseModel, Field


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