from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    name: str = Field(examples=["会社名"])
    prefecture: str = Field(examples=["都道府県"])
    city: str = Field(examples=["市区町村"])
    town: str = Field(examples=["町名、番地等"])
    address: str = Field(examples=["建物名、部屋番号等"])
    postal_code: str = Field(examples=["郵便番号"])
    phone_number: str = Field(examples=["電話番号"])
    email: str = Field(examples=["メールアドレス"])


class ResponseBody(BaseModel):
    company_id: int
    name: str
    prefecture: str
    city: str
    town: str
    address: str
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