from typing import Optional
from pydantic import BaseModel, Field


class RequestList(BaseModel):
    role:Optional[str] = Field(default=None, examples=["student"])
    page:int = Field(default=None, examples=[1],gt=0)
    limit:int = Field(default=None, examples=[10],gt=0)

class ResponseList(BaseModel):
    user_id: int = Field(gt=0, examples=[1])
    first_name: str = Field(examples=["太郎"])
    last_name: str = Field(examples=["田中"])
    email: str = Field(examples=["taro@example.com"])
    role: str = Field(examples=["student"])
    last_login: str

class ResponseBody(BaseModel):
    users: list[ResponseList]