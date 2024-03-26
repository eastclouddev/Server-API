from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class ResponseBody(BaseModel):
    curriculum_id: int
    title: str
    description: str
    video_url: str
    content: str 
    is_test: bool
    display_no: int
    