from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.company_receipts import CompanyReceipts

def find_billing_summary(db: Session):
    today = datetime.today()
    month = 12 if today.month == 1 else today.month - 1
    year = today.year - 1 if today.month == 1 else today.year
    last_month_str = str(year) + "-" + str(month).zfill(2)
    
    company_receipts = db.query(CompanyReceipts)\
                        .filter(CompanyReceipts.payment_date.contains(last_month_str)).all()

    total_billed_amount = 0
    for company_receipt in company_receipts:
        total_billed_amount += company_receipt.amount

    di = {
        "month": last_month_str,
        "total_billed_amount": total_billed_amount
    }

    return di