from typing import Optional
from pydantic import BaseModel, Field


class PasswordResetRequest(BaseModel):
    email: Optional[str] = Field(None, examples=["Sample@mail.com"])


class PasswordResetConfirm(BaseModel):
    token: Optional[str] = Field(None, examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1haWxBQG1haWwuY29tIn0.8bs36F_c_bXN3sRGXPYk46TixH7hg0yIh9pxKtW1biU"])
    new_password: Optional[str] = Field(None, examples=["NewPass1234!"])
