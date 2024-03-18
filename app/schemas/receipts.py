from typing import Optional
from pydantic import BaseModel, Field


class ResponseBody(BaseModel):
    receipt_id: int
    company_id: int
    billing_id: int
    date: str
    amount: float
    received_from: str
    payment_method: str
