from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateRequestBody(BaseModel):
    user_id: int = Field(examples=[1])
    parent_response_id: Optional[int] = Field(examples=[1])
    content: str = Field(examples=["回答の内容"])
    is_read: bool = Field(examples=[False])

class CreateResponseBody(BaseModel):
    id: int
    review_request_id: int
    user_id: int
    parent_response_id: Optional[int]
    content: str
    is_read: bool
    created_at: str

class RequestBody(BaseModel):
    content: Optional[str] = Field(examples=["content"])
    is_read: Optional[bool] = Field(examples=[False])



class ResponseBody(BaseModel):
    id: int
    review_request_id: int
    user_id: int
    parent_response_id: int
    content: str
    is_read: bool
    updated_at: str