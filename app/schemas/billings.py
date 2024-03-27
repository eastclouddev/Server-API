from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass

class Payment(BaseModel):
    payment_method: str
    payment_date: str 

class DetailonseBody(BaseModel):
    billing_id: int
    company_id: int
    date: str
    amount: float
    status: str
    payment_details: Optional[Payment] = None