from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class QuizContent(BaseModel):
    quiz_id: int
    question: str
    media_content: Optional[list] = None
    options: dict
    correct_answer: int
    explanation: str

class CurriculumDetailResponseBody(BaseModel):
    curriculum_id: int
    title: str
    description: str
    video_url: Optional[str] = None
    content: Optional[str] = None
    is_quiz: bool
    quiz_content: Optional[list[QuizContent]] = None
    display_no: int

