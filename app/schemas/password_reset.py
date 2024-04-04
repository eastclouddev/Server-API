from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class ResponseBody(BaseModel):
    pass

class PasswordResetRequest(BaseModel):
    email: Optional[str]


class PasswordResetConfirm(BaseModel):
    token: Optional[str] = Field(None, examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haWxBQG1haWwuY29tIn0.8bs36F_c_bXN3sRGXPYk46TixH7hg0yIh9pxKtW1biU"])
    new_password: Optional[str] = Field(None, examples=["NewPass1234!"])
