from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Course(BaseModel):
    course_id: int
    title: str
    description: str
    created_user: int
    thumbnail_url: str
    created_at: str

class ResponseBody(BaseModel):
    courses: list[Course]