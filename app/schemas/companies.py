from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreateRequestBody(BaseModel):
    name: str = Field(examples=["会社名"])
    prefecture: str = Field(examples=["都道府県"])
    city: str = Field(examples=["市区町村"])
    town: str = Field(examples=["町名、番地等"])
    address: Optional[str] = Field(None, examples=["建物名、部屋番号等"])
    postal_code: str = Field(examples=["郵便番号"])
    phone_number: str = Field(examples=["電話番号"])
    email: str = Field(examples=["メールアドレス"])

class CompanyCreateResponseBody(BaseModel):
    company_id: int
    name: str
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    postal_code: str
    phone_number: str
    email: str

class CompanyDetailResponseBody(BaseModel):
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

class CompanyListResponseBody(BaseModel):
    companies: list[Company]

class ProgressesResponseList(BaseModel):
    progress_id: int
    user_id: int
    course_id: int
    section_id: Optional[int]
    curriculum_id: Optional[int]
    progress_percentage: int
    status: str

class ProgressListResponseBody(BaseModel):
    progresses: list[ProgressesResponseList]


class Student(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    role: str
    last_login: str

class StudentListResponseBody(BaseModel):
    users: list[Student]