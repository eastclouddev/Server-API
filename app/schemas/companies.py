from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateRequestBody(BaseModel):
    name: str = Field(examples=["会社名"])
    prefecture: str = Field(examples=["都道府県"])
    city: str = Field(examples=["市区町村"])
    town: str = Field(examples=["町名、番地等"])
    address: Optional[str] = Field(None, examples=["建物名、部屋番号等"])
    postal_code: str = Field(examples=["郵便番号"])
    phone_number: str = Field(examples=["電話番号"])
    email: str = Field(examples=["メールアドレス"])

class CreateResponseBody(BaseModel):
    company_id: int
    name: str
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    postal_code: str
    phone_number: str
    email: str

class DetailResponseBody(BaseModel):
    company_id: int
    name: str
    prefecture: str
    city: str
    town: str
    address: str
    postal_code: str
    phone_number: str
    email: str
    created_at: str
    updated_at: str

class Company(BaseModel):
    company_id: int
    name: str 
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    postal_code: str
    phone_number: str
    email: str
    created_at: str

class AllResponseBody(BaseModel):
    companies: list[Company]


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
  