from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    user_id: int
    name: str

class AnswerCreateRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    parent_answer_id: int = Field(None, examples=[1])
    content: str = Field(examples=["内容を記載"])
    media_content: list = Field(None, examples=[[{"url": "hoge"}, {"url": "moge"}]])

class AnswerCreateResponseBody(BaseModel):
    answer_id: int
    question_id: int
    parent_answer_id: Optional[int]
    user: User
    content: str
    media_content: Optional[list]
    created_at: str

class ResponseQuestion(BaseModel):
    id: int
    curriculum_id: int
    user: User
    title: str
    objective: str
    current_situation: str
    research: str    
    content: str
    media_content: Optional[list]
    is_closed: bool
    created_at: str

class ResponseList(BaseModel):
    id: int
    question_id: int
    user: User
    parent_answer_id: Optional[int]
    content: str
    media_content: Optional[list]
    created_at: str

class QuestionThreadDetailResponseBody(BaseModel):
    question: ResponseQuestion
    answer: list[ResponseList]

class QuestionUpdateRequestBody(BaseModel):
    title: Optional[str] = Field(examples=["更新されたタイトル"])
    content: Optional[str] = Field(examples=["更新する内容"])
    media_content: Optional[dict] = Field(examples=[])
    is_closed: bool

class QuestionUpdateResponseBody(BaseModel):
    id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    media_content: Optional[dict]
    is_closed: bool
    updated_at: str

class AnswerUpdateRequestBody(BaseModel):
    content: Optional[str] = Field(examples=["更新する内容"])
    media_content: Optional[dict] = Field(examples=[])
    is_read: bool

class AnswerUpdateResponseBody(BaseModel):
    id: int
    question_id: int
    user_id: int
    parent_answer_id: Optional[int]
    content: str
    media_content: Optional[dict]
    is_read: bool
    updated_at: str