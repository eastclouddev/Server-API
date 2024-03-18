from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    company_id: int = Field(gt=0, examples=[1])
    first_name: str = Field(min_length=2, max_length=20, examples=["NAME"])
    last_name: str = Field(min_length=2, max_length=20, examples=["NAME"])
    first_name_kana: str = Field(min_length=2, max_length=20, examples=["NAME"])
    last_name_kana: str = Field(min_length=2, max_length=20, examples=["NAME"])
    password: str = Field(min_length=6, max_length=64, example="password123")
    email: str = Field(example="taro.yamada@example.com")
    role_id: int = Field(gt=0, examples=[1])

class UserResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    company_id: int = Field(gt=0, examples=[1])
    first_name: str = Field(min_length=2, max_length=20, examples=["NAME"])
    last_name: str = Field(min_length=2, max_length=20, examples=["NAME"])
    first_name_kana: str = Field(min_length=2, max_length=20, examples=["NAME"])
    last_name_kana: str = Field(min_length=2, max_length=20, examples=["NAME"])
    email: str = Field(example="taro.yamada@example.com")
    role_id: int = Field(gt=0, examples=[1])
    is_enable: bool = Field(default=True, example=True)
    is_logged_in: bool = Field(default=True, example=True)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

