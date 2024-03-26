from typing import Optional
from pydantic import BaseModel, Field



class RequestBody(BaseModel):
    title: Optional[str] = Field(examples=["title"])
    content: Optional[str] = Field(examples=["content"])
    is_closed: Optional[bool] = Field(examples=[False])



class ResponseBody(BaseModel):
    id: int
    title: str
    content: str
    is_closed: bool
    updated_at: str