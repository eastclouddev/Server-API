from sqlalchemy.orm import Session
from models.company_billing_info import CompanyBillingInfo
from models.payment_methods import PaymentMethods
from models.company_receipts import CompanyReceipts 
from models.company_transaction_histories import CompanyTransactionHistories 
from models.company_billing_statuses import CompanyBillingStatuses


def find_by_detail(db: Session, billing_id: int):
    billing_info = db.query(CompanyBillingInfo).filter(CompanyBillingInfo.id == billing_id).first()
    if not billing_info:
        print("billing_info")
        return None
    company_id = billing_info.company_id

    payment_method = db.query(PaymentMethods).filter(billing_info.payment_method_id == PaymentMethods.id).first()
    if not payment_method :
        print("payment_method")
        return None
    payment_methods = payment_method.name

    company_receipt = db.query(CompanyReceipts).filter(billing_info.id == CompanyReceipts.billing_info_id).first()
    if not company_receipt:
        print("company_receipt")
        return None
    amount = company_receipt.amount
    pre_payment_date = company_receipt.payment_date
    payment_date = pre_payment_date.strftime("%Y-%m-%d")

    transaction_history = db.query(CompanyTransactionHistories).filter(billing_info.id == CompanyTransactionHistories.billing_info_id).first()
    if not transaction_history:
        print("trnsaction_history")
        return None
    pre_date = transaction_history.invoice_date
    date = pre_date.strftime("%Y-%m-%d")

    billing_status = db.query(CompanyBillingStatuses).filter(transaction_history.billing_status_id == CompanyBillingStatuses.id).first()
    if not billing_status:
        print("billing_status")
        return None
    status = billing_status.name

    #請求履歴詳細
    info = {
        "billing_id": billing_id,
        "company_id": company_id,
        "date": date,
        "amount": amount,
        "status": status
    }

    #支払い済みの時にだけ返す支払い詳細
    payment_details = {

        "payment_details": {
        "payment_method": payment_methods,
        "payment_date": payment_date
        } 
    }

    # 支払い完了の場合に支払いお詳細を表示
    if status == "paid":
    
        #infoに支払い詳細を追加
        info.update(payment_details)

    return info