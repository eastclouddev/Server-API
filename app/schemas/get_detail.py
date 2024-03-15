from pydantic import BaseModel


class ResponsePayment(BaseModel):
    payment_methods: str
    payment_date: str 


class ResponseBilling(BaseModel):
    billing_id: int
    company_id: int
    date: str
    amount: float
    status: str
    payment_details: ResponsePayment