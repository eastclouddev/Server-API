from typing import Optional
from pydantic import BaseModel, Field

class AllResponseList(BaseModel):
    company_id: int
    name: str 
    prefecture: str
    city: str
    town: str
    address: str
    postal_code: str
    phone_number: str
    email: str
    created_at: str

class AllResponseBody(BaseModel):
    companies: list[AllResponseList]