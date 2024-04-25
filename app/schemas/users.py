from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserUpdateRequestBody(BaseModel):
    first_name: Optional[str] = Field(None, examples=["花子"])
    last_name: Optional[str] = Field(None, examples=["山田"])
    first_name_kana: Optional[str] = Field(None, examples=["ハナコ"])
    last_name_kana: Optional[str] = Field(None, examples=["ヤマダ"])
    email: Optional[str] = Field(None, examples=["hanako@example.com"])

class UserDetailResponseBody(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    first_name_kana: str
    last_name_kana: str
    email: str
    role: str
    last_login: str  

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str
    last_login: str 

class UserListResponseBody(BaseModel):
    users: list[User]