from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RequestBody(BaseModel):
    pass


class DetailResponseBody(BaseModel):
    mentor_id: int
    account_name: str
    bank_name: str
    branch_name: str
    account_number: str
    account_type: str