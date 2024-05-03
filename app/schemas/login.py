from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceInfo(BaseModel):
    device_type: Optional[str] = Field(None, examples=["smartphone"])
    device_name: Optional[str] = Field(None, examples=["iPhone 12"])
    uuid: Optional[str] = Field(None, examples=["generated_uuid"])

class RequestBody(BaseModel):
    email: Optional[str] = Field(None, examples=["user@example.com"])
    password: Optional[str] = Field(None, examples=["password123"])
    device_info: DeviceInfo

class ResponseBody(BaseModel):
    user_id: int
    access_token: str
    expires_in: int
    role: str

class LoginRequestBody(BaseModel):
    email: Optional[str] = Field(examples=["aaa@mail.com"])
    password: Optional[str] = Field(examples=["test1234"])
    device_info: DeviceInfo