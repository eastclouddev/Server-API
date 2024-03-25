from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class ResponseBody(BaseModel):
    id: int
    title: str
    summary: str
    content: str
    published_at: str