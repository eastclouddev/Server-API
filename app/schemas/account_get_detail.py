from datetime import datetime
from enum import Enum
from typing import  Optional
from pydantic import BaseModel,Field,ConfigDict

class Responsebody(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    first_name_kana: str
    last_name_kana: str
    email: str
    role: str
    last_login: str  
