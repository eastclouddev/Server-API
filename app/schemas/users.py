from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreateRequestBody(BaseModel):
    first_name: Optional[str] = Field(None, examples=["花子"])
    last_name: Optional[str] = Field(None, examples=["山田"])
    first_name_kana: Optional[str] = Field(None, examples=["ハナコ"])
    last_name_kana: Optional[str] = Field(None, examples=["ヤマダ"])
    email: Optional[str] = Field(None, examples=["hanako@example.com"])
    role: Optional[str] = Field(None, examples=["student"])
    company_id: Optional[int] = Field(None, examples=[1])

class UserCreateResponseBody(BaseModel):
    user_id: int

class UserUpdateRequestBody(BaseModel):
    first_name: Optional[str] = Field(None, examples=["花子"])
    last_name: Optional[str] = Field(None, examples=["山田"])
    first_name_kana: Optional[str] = Field(None, examples=["ハナコ"])
    last_name_kana: Optional[str] = Field(None, examples=["ヤマダ"])
    email: Optional[str] = Field(None, examples=["hanako@example.com"])
    is_enable: Optional[bool] = Field(True, examples=[True])

class UserDetailResponseBody(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    first_name_kana: str
    last_name_kana: str
    email: str
    company_name: str
    is_enable: bool
    role: str
    last_login: str  

class User(BaseModel):
    user_id: int
    name: str
    company_name: str
    email: str
    role: str
    is_enable: bool
    last_login: str 

class UserListResponseBody(BaseModel):
    users: list[User]

class Role(BaseModel):
    role_id: int
    role_name: str
    count: int

class AccountListResponseBody(BaseModel):
    role_counts: list[Role]