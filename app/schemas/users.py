
from typing import Optional
from pydantic import BaseModel, Field


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, examples=["花子"])
    last_name: Optional[str] = Field(None, examples=["山田"])
    first_name_kana: Optional[str] = Field(None, examples=["ハナコ"])
    last_name_kana: Optional[str] = Field(None, examples=["ヤマダ"])
    email: Optional[str] = Field(None, examples=["hanako@example.com"])
