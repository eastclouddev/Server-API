from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class RequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    content: str = Field(examples=["内容を記載"])


class ResponseBody(BaseModel):
    answer_id: int
    question_id: int
    user_id: int
    content: str
