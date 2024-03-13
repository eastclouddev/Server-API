from pydantic import Field, BaseModel
from typing import Optional


class DeviceInfo(BaseModel):
    device_type: Optional[str] = Field(None, examples=["smartphone"])
    device_name: Optional[str] = Field(None, examples=["iPhone 12"])
    uuid: Optional[str] = Field(None, examples=["generated_uuid"])

class RequestBody(BaseModel):
    email: Optional[str] = Field(None, examples=["user@example.com"])
    password: Optional[str] = Field(None, examples=["password123"])
    device_info: DeviceInfo

