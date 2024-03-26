from datetime import datetime
from enum import Enum
from typing import  Optional
from pydantic import BaseModel,Field,ConfigDict

class Progress(BaseModel):
    course_id: int
    course_title: str
    progress_percentage: int
    status: str
    last_accessed_at: str

class ResponseBody(BaseModel):
    progresses:list[Progress]