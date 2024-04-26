from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProgressesResponseList(BaseModel):
    progress_id: int
    user_id: int
    course_id: int
    section_id: Optional[int]
    curriculum_id: Optional[int]
    progress_percentage: int
    status: str

class ProgressListResponseBody(BaseModel):
    progresses: list[ProgressesResponseList]
