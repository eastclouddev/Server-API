from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class BillingSummaryResponseBody(BaseModel):
    month: str
    total_billed_amount: Union[int, float]