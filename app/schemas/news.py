from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class CreateRequestBody(BaseModel):
    title: str = Field(examples=["Newsのタイトル"])
    content: str = Field(examples=["Newsの内容"])
    is_published: bool = Field(examples=[False])
    published_at: str = Field(examples=["2024-03-01T10:00:00"])

class CreateResponseBody(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    published_at: str
    created_at: str

class DetailResponseBody(BaseModel):
    id: int
    title: str
    content: str
    published_at: str

class News(BaseModel):
    id: int
    title: str
    published_at: str

class AllResponseBody(BaseModel):
    news:list[News]
    page: int
    limit: int
    total_pages: int
    total_news: int 
      