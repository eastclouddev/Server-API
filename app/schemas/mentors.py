from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Rewards(BaseModel):
    reward_id: int
    date: str
    amount: float
    to_mentor_id: int

class ResponseBody(BaseModel):
    rewards: list[Rewards]