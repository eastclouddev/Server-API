from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class ResponseBody(BaseModel):
    receipt_id: int
    company_id: int
    billing_id: int
    date: str
    amount: float
    received_from: str
    payment_method: str