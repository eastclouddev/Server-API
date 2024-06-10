from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CurriculumDetailResponseBody(BaseModel):
    curriculum_id: int
    title: str
    description: str
    video_url: Optional[str] = None
    content: Optional[str] = None
    is_test: bool
    display_no: int

