from pydantic import BaseModel
from pydantic import Field

class ResponseBodyGet(BaseModel):
    mentor_id: int
    account_name: str
    bank_name: str
    branch_name: str
    account_number: str
    account_type: str


