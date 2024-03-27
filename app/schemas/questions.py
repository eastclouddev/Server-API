from typing import Optional
from pydantic import BaseModel, Field


class MediaContent(BaseModel):
    url: str

class RequestBody(BaseModel):
    user_id: int
    title: str
    content: str
    media_content: MediaContent

class ResponseBody(BaseModel):
    question_id: int
    curriculum_id: int
    user_id: int
    title: str
    content: str
    media_content: list