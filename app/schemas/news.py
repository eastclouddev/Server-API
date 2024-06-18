from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NewsUpdateRequestBody(BaseModel):
    title: str = Field(None,examples=["タイトル"])
    content: str = Field(None,examples=["内容"])
    category_id: int = Field(examples=["カテゴリのID"])
    is_published: bool = Field(None,examples=[True])
    published_at: str = Field(None,examples=["2023-03-01T10:00:00Z"])

class NewsResponse(BaseModel):
    category_id: int
    category_name: str

class Category(BaseModel):
    category_id: int
    category_name: str

class News(BaseModel):
    id: int
    title: str
    category: Category
    published_at: str

class NewsListResponseBody(BaseModel):
    news: list[News]
      
class NewsUpdateResponseBody(BaseModel):
    news_id: int
    title: str
    content: str
    category: NewsResponse
    is_published: bool
    published_at: str
    updated_at: str

class NewsCreateRequestBody(BaseModel):
    title: str = Field(examples=["Newsのタイトル"])
    content: str = Field(examples=["Newsの内容"])
    category_id: int = Field(examples=["カテゴリのID"])
    published_at: str = Field(examples=["2024-03-01T10:00:00"])
    
class NewsCreateResponseBody(BaseModel):
    id: int
    title: str
    content: str
    category: NewsResponse
    is_published: bool
    published_at: str
    created_at: str

class NewsDetailResponseBody(BaseModel):
    id: int
    title: str
    content: str
    category: Category
    published_at: str

class NewsCategoryUpdateRequestBody(BaseModel):
    name: str = Field(examples=["ニュースカテゴリの名前"])

class NewsCategoryRequestBody(BaseModel):
    name: str = Field(examples=["ニュースカテゴリの名前"])

class NewsCategory(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

class NewsCategoryUpdateResponseBody(BaseModel):
    message: str
    category: NewsCategory

class NewsCategoryResponseBody(BaseModel):
    message: str
    category: NewsCategory

class NewsCategoryListResponseBody(BaseModel):
    categories: list[NewsCategory]

class NewsBody(BaseModel):
    id: int
    title: str
    category: NewsResponse
    published_at: str

class PublishedNewsListResponseBody(BaseModel):
    news: list[NewsBody]