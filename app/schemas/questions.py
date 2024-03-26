from typing import Optional
from pydantic import BaseModel, Field

class ResponseQuestion(BaseModel):
    id:int
    curriculum_id:int
    user_id:int
    title:str
    content:str
    media_content:dict
    is_closed:bool
    created_at:str

class ResponseList(BaseModel):
    id:int
    question_id: int
    user_id:int
    parent_answer_id:Optional[int]
    content: str
    media_content:dict
    is_read: bool
    created_at: str

class ResponseBody(BaseModel):
    question:ResponseQuestion
    answer: list[ResponseList]