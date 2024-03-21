from pydantic import BaseModel, Field

class RequestBody(BaseModel):
    bank_name: str = Field(examples=["銀行名"])
    branch_name: str = Field(examples=["支店名"])
    bank_code: str = Field(examples=["銀行コード"])
    branch_code: str = Field(examples=["支店コード"])
    account_type: str = Field(examples=["口座種別 ordinary (普通), current (当座), savings (貯蓄)"])
    account_number: str = Field(examples=["口座番号"])
    account_name: str = Field(examples=["口座名義"])

class ResponseBody(BaseModel):
    account_id: int
    mentor_id: int 
    bank_name: str
    branch_name: str
    bank_code: str
    branch_code: str
    account_type: str
    account_number: str
    account_name: str