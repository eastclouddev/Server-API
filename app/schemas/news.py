from datetime import datetime
from enum import Enum
from typing import  Optional
from pydantic import BaseModel,Field,ConfigDict

class News(BaseModel):
    id: int
    title: str
    published_at: str

class ResponsBody(BaseModel):
    news:list[News]
    page: int
    limit: int
    total_pages: int
    total_news: int 
    
