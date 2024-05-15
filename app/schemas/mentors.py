from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class AccountInfoDetailResponseBody(BaseModel):
    mentor_id: int
    account_name: str
    bank_name: str
    branch_name: str
    account_number: str
    account_type: str

class AccountInfoCreateRequestBody(BaseModel):
    bank_name: str = Field(examples=["銀行名"])
    branch_name: str = Field(examples=["支店名"])
    bank_code: str = Field(examples=["銀行コード"])
    branch_code: str = Field(examples=["支店コード"])
    account_type: str = Field(examples=["口座種別 ordinary (普通), current (当座), savings (貯蓄)"])
    account_number: str = Field(examples=["口座番号"])
    account_name: str = Field(examples=["口座名義"])

class Rewards(BaseModel):
    reward_id: int
    date: str
    amount: float
    to_mentor_id: int

class RewardListResponseBody(BaseModel):
    rewards: list[Rewards]

class AccountInfoCreateResponseBody(BaseModel):
    account_id: int
    mentor_id: int 
    bank_name: str
    branch_name: str
    bank_code: str
    branch_code: str
    account_type: str
    account_number: str
    account_name: str

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

class Question(BaseModel):
    id: int
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool

class QuestionListResponseBody(BaseModel):
    questions: list[Question]

class AllResponseList(BaseModel):
    id: int 
    title: str
    content: str
    curriculum_id: int
    created_at: str
    is_read: bool
    is_closed: bool

class ReviewRequestListResponseBody(BaseModel):
    reviews: list[AllResponseList]

class MentorScountResponseBody(BaseModel):
    mentor_id: int
    mentor_name: str
    student_count: int

class MentorScountList(BaseModel):
    mentors: list[MentorScountResponseBody]
