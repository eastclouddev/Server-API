from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["株式会社テスト"])
    prefecture: str = Field(min_length=2, max_length=50, examples=["東京都"])
    city: str = Field(min_length=2, max_length=100, examples=["渋谷区"])
    town: str = Field(min_length=2, max_length=255, examples=["Test1-2-3"])
    address: str = Field(min_length=6, max_length=255, example="TestBuilding5F")
    postal_code: str = Field(max_length=10, example="150-0041")
    phone_number: str = Field(max_length=20, example="03-1234-5678")
    email: str = Field(max_length=255, example="taro.yamada@example.com")

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(min_length=2, max_length=100, examples=["株式会社テスト"])
    prefecture: Optional[str] = Field(min_length=2, max_length=50, examples=["東京都"])
    city: Optional[str] = Field(min_length=2, max_length=100, examples=["渋谷区"])
    town: Optional[str] = Field(min_length=2, max_length=255, examples=["Test1-2-3"])
    address: Optional[str] = Field(min_length=6, max_length=255, example="TestBuilding5F")
    postal_code: Optional[str] = Field(max_length=10, example="150-0041")
    phone_number: Optional[str] = Field(max_length=20, example="03-1234-5678")
    email: Optional[str] = Field(max_length=255, example="taro.yamada@example.com")

class CompanyResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=100, examples=["株式会社テスト"])
    prefecture: str = Field(min_length=2, max_length=50, examples=["東京都"])
    city: str = Field(min_length=2, max_length=100, examples=["渋谷区"])
    town: str = Field(min_length=2, max_length=255, examples=["Test1-2-3"])
    address: str = Field(min_length=6, max_length=255, example="TestBuilding5F")
    postal_code: str = Field(max_length=10, example="150-0041")
    phone_number: str = Field(max_length=20, example="03-1234-5678")
    email: str = Field(max_length=255, example="taro.yamada@example.com")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

