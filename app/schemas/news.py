from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    title: str = Field(None,examples=["タイトル"])
    content: str = Field(None,examples=["内容"])
    is_published: bool = Field(None,examples=[True])
    published_at: str = Field(None,examples=["2023-03-01T10:00:00Z"])
    
class ResponseBody(BaseModel):
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
      
class UpdateResponseBody(BaseModel):
    news_id: int
    title: str
    content: str
    is_published: bool
    published_at: str
    updated_at: str
