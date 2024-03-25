from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    title: str = Field(examples=["Newsのタイトル"])
    content: str = Field(examples=["Newsの内容"])
    is_published: bool = Field(examples=[False])
    published_at: str = Field(examples=["2024-03-01T10:00:00"])


class ResponseBody(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    published_at: str
    created_at: str