from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ResponseBody(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    published_at: str
