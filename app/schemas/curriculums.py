from pydantic import BaseModel


class ResponseBody(BaseModel):
    curriculum_id: int
    title: str
    description: str
    video_url: str
    content: str 
    is_test: bool
    display_no: int
    