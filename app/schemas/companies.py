from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreateRequestBody(BaseModel):
    name: str = Field(examples=["会社名"])
    name_kana: str = Field(examples=["会社名フリガナ"])
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
    name_kana: str
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    postal_code: str
    phone_number: str
    email: str

class CompanyUpdateRequestBody(BaseModel):
    name: Optional[str] = Field(examples=["会社名"])
    name_kana: Optional[str] = Field(examples=["シャメイ"])
    prefecture: Optional[str] = Field(examples=["都道府県"])
    city: Optional[str] = Field(examples=["市区町村"])
    town: Optional[str] = Field(examples=["町名、番地等"])
    address: Optional[str] = Field(None, examples=["建物名、部屋番号等"])
    postal_code: Optional[str] = Field(examples=["郵便番号"])
    phone_number: Optional[str] = Field(examples=["電話番号"])
    email: Optional[str] = Field(examples=["メールアドレス"])

class CompanyUpdateResponseBody(BaseModel):
    company_id: int
    name: str
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    postal_code: str
    phone_number: str
    email: str
    updated_at: datetime

class CompanyDetailResponseBody(BaseModel):
    company_id: int
    name: str
    name_kana: str
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
    name_kana: str 
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
    user_id: int
    user_name: str
    course_id: int
    course_name: str
    section_id: Optional[int]
    curriculum_id: Optional[int]
    progress_percentage: int
    status: str

class ProgressListResponseBody(BaseModel):
    progresses: list[ProgressesResponseList]


class Student(BaseModel):
    user_id: int
    name: str
    email: str
    role: str
    is_enable: bool
    last_login: str

class StudentListResponseBody(BaseModel):
    users: list[Student]

class Billing(BaseModel):
    billing_id: int
    date: str
    amount: float
    status: str
    description: str

class BillingListResponseBody(BaseModel):
    billings: list[Billing]

class Account(BaseModel):
    role_id: int
    role_name: str
    count: int

class AccountListResponseBody(BaseModel):
    company_id: int
    role_counts: list[Account]

class CompanyBillingInfoCreateRequestBody(BaseModel):
    prefecture: str = Field(examples=["都道府県"])
    city: str = Field(examples=["市区町村"])
    town: str = Field(examples=["町名、番地等"])
    address: Optional[str] = Field(None, examples=["建物名、部屋番号等"])
    billing_email: str = Field(examples=["メールアドレス"])
    invoice_number: str = Field(examples=["xxx"])
    tax_number: str = Field(examples=["xxx"])
    payment_method_id: int = Field(examples=[1])
    notes: Optional[str] = Field(None, examples=["メモ"])
    last_receipt_number: Optional[str] = Field(None, examples=["xxx"])

class CompanyBillingInfoCreateResponseBody(BaseModel):
    id: int
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    billing_email: str
    invoice_number: str
    tax_number: str
    payment_method_id: int
    notes: Optional[str]
    last_receipt_number: Optional[str]
    created_at: datetime

class CompanyBillingInfoUpdateRequestBody(BaseModel):
    prefecture: str = Field(examples=["都道府県"])
    city: str = Field(examples=["市区町村"])
    town: str = Field(examples=["町名、番地等"])
    address: Optional[str] = Field(None, examples=["建物名、部屋番号等"])
    billing_email: str = Field(examples=["メールアドレス"])
    invoice_number: str = Field(examples=["xxx"])
    tax_number: str = Field(examples=["xxx"])
    payment_method_id: int = Field(examples=[1])
    notes: Optional[str] = Field(None, examples=["メモ"])
    last_receipt_number: Optional[str] = Field(None, examples=["xxx"])
    updated_at: str

class CompanyBillingInfoUpdateResponseBody(BaseModel):
    id: int
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    billing_email: str
    invoice_number: str
    tax_number: str
    payment_method_id: int
    notes: Optional[str]
    last_receipt_number: Optional[str]
    created_at: str
    updated_at: str

class CompanyBillingInfoDetailResponseBody(BaseModel):
    id: int
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    billing_email: str
    invoice_number: str
    tax_number: str
    payment_method: str
    description: Optional[str]
    notes: Optional[str]
    last_receipt_number: Optional[str]
    created_at: str
    updated_at: str

class CompanyBillingInfo(BaseModel):
    prefecture: str
    city: str
    town: str
    address: Optional[str]
    billing_email: str
    invoice_number: str
    tax_number: str
    payment_method_id: int
    notes: Optional[str]
    last_receipt_number: Optional[str]
    created_at: str
    updated_at: str