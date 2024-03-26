from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


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
      