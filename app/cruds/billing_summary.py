from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.company_receipts import CompanyReceipts
from models.company_transaction_histories import CompanyTransactionHistories

def find_billing_summary(db: Session):
    #現在の先月を調べる
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_month_last_day = first_day_of_current_month - timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)
    
    last_month_str = last_month_first_day.strftime("%Y-%m")
    
    #現在の先月に紐ずくamountを呼び出す
    company_receipts = db.query(CompanyReceipts).filter(CompanyReceipts.payment_date >= last_month_first_day,
        CompanyReceipts.payment_date <= last_month_last_day
    ).all()

    total_billed_amount = 0
    for company_receipt in company_receipts:
        total_billed_amount += company_receipt.amount
    di = {
        "month": last_month_str,
        "total_billed_amount": total_billed_amount
    }

    return di