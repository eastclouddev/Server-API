from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestList(BaseModel):
    user_id: int 

class ResponseList(BaseModel):
    id: int
    title: str
    content: str
    curriculum_id: int
    created_at: datetime
    is_read: bool
    is_closed: bool
      
    

class ResponseBody(BaseModel):
    questions: list[ResponseList]