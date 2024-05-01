from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NewsUpdateRequestBody(BaseModel):
    title: str = Field(None,examples=["タイトル"])
    content: str = Field(None,examples=["内容"])
    is_published: bool = Field(None,examples=[True])
    published_at: str = Field(None,examples=["2023-03-01T10:00:00Z"])

class News(BaseModel):
    id: int
    title: str
    published_at: str

class NewsListResponseBody(BaseModel):
    news:list[News]
    page: int
    limit: int
    total_pages: int
    total_news: int 
      
class NewsUpdateResponseBody(BaseModel):
    news_id: int
    title: str
    content: str
    is_published: bool
    published_at: str
    updated_at: str

class NewsCreateRequestBody(BaseModel):
    title: str = Field(examples=["Newsのタイトル"])
    content: str = Field(examples=["Newsの内容"])
    is_published: bool = Field(examples=[False])
    published_at: str = Field(examples=["2024-03-01T10:00:00"])
    
class NewsCreateResponseBody(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    published_at: str
    created_at: str

class NewsDetailResponseBody(BaseModel):
    id: int
    title: str
    content: str
    published_at: str