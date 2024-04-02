from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class ResponseBody(BaseModel):
    pass

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=["NAME"])
    price: int = Field(gt=0, examples=[9999])
    description: Optional[str] = Field(None, examples=["description"])

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=20, examples=["NAME"])
    price: Optional[int] = Field(None, gt=0, examples=[9999])
    description: Optional[str] = Field(None, examples=["description"])

class ProductResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=20, examples=["NAME"])
    price: int = Field(gt=0, examples=[9999])
    description: Optional[str] = Field(None, examples=["description"])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)