from typing import Optional
from pydantic import BaseModel, Field



class RiquestBody(BaseModel):
    content: Optional[str] = Field(examples=["content"])
    is_read: Optional[bool] = Field(examples=[False])



class ResponseBody(BaseModel):
    id: int
    review_request_id: int
    user_id: int
    parent_response_id: int
    content: str
    is_read: bool
    updated_at: str