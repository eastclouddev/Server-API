from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.companies import CompanyCreateRequestBody, CompanyCreateResponseBody, CompanyDetailResponseBody, \
CompanyUpdateRequestBody, CompanyBillingInfoUpdateResponseBody, CompanyBillingInfoCreateRequestBody, CompanyBillingInfoCreateResponseBody, \
CompanyBillingInfoDetailResponseBody, CompanyBillingInfoUpdateRequestBody, CompanyBillingInfoUpdateResponseBody, \
CompanyListResponseBody, StudentListResponseBody, ProgressListResponseBody, \
                                BillingListResponseBody, AccountListResponseBody
from cruds import companies as companies_cruds
from services import companies as compamies_services

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=CompanyCreateResponseBody, status_code=status.HTTP_200_OK)
async def create_company(db: DbDependency, param: CompanyCreateRequestBody):
    """
    会社情報作成

    Parameters
    -----------------------
    dict
        name: str
            会社名
        name_kana: str
            会社名フリガナ
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        postal_code: str
            郵便番号
        phone_number: str
            電話番号
        email: str
            メールアドレス

    Returns
    -----------------------
    dict
        company_id: int
            新しく作成された会社のID
        name: str
            会社名
        name_kana: str
            会社名フリガナ
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        postal_code: str
            郵便番号
        phone_number: str
            電話番号
        email: str
            メールアドレス
    """

    # TODO:メールアドレスの重複チェックが入る予定（emailがuniqueになったため）

    try:
        new_company = companies_cruds.create_company(db, param)
            
        db.commit()
        
        re_di = {
            "company_id": new_company.id,
            "name": new_company.name,
            "name_kana": new_company.name_kana,
            "prefecture": new_company.prefecture,
            "city": new_company.city,
            "town": new_company.town,
            "address": new_company.address,
            "postal_code": new_company.postal_code,
            "phone_number": new_company.phone_number,
            "email": new_company.email
        }

        return re_di
    
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{company_id}", response_model=CompanyDetailResponseBody, status_code=status.HTTP_200_OK)
async def find_company_details(db: DbDependency, company_id: int = Path(gt=0)):
    """
    会社詳細取得

    Parameter
    -----------------------
    company_id: int
        詳細情報を取得したい会社のID

    Returns
    -----------------------
    dict
        company_id: int
            会社のID
        name: str
            会社の名前
        name: str
            会社名のフリガナ
        prefecture: str
            所在地の都道府県
        city: str
            所在地の市区町村
        town: str
            所在地の町名・番地等
        address: str
            会社の詳細な住所
        postal_code: str
            郵便番号
        phone_number: str
            電話番号
        email: str
            会社のメールアドレス
        created_at: str
            レコードの作成日時（ISO 8601形式）
        updated_at: str
            レコードの最終更新日時（ISO 8601形式）

    """
    company = companies_cruds.find_company_by_company_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    info = {
        "company_id": company_id,
        "name": company.name,
        "name_kana": company.name_kana,
        "prefecture": company.prefecture,
        "city": company.city,
        "town": company.town,
        "address": company.address,
        "postal_code": company.postal_code,
        "phone_number": company.phone_number,
        "email": company.email,
        "created_at": company.created_at.isoformat(),
        "updated_at": company.updated_at.isoformat()
    }

    return info


@router.patch("/{company_id}", status_code=status.HTTP_200_OK)
async def update_company(db: DbDependency, param: CompanyUpdateRequestBody, company_id: int = Path(gt=0)):
    """
    会社情報更新

    Parameters
    -----------------------
    company_id: int
        会社情報のID
    dict
        name: str
            会社名
        name_kana: str
            会社名フリガナ
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        postal_code: str
            郵便番号
        phone_number: str
            電話番号
        email: str
            メールアドレス

    Returns
    -----------------------
    message: str
        完了時のメッセージ(Company information updated successfully.)
    """

    update_company = companies_cruds.update_company(db, param, company_id)
    if not update_company:
        raise HTTPException(status_code=404, detail="Company not found.")

    try:
        db.commit()
        return {"message": "Company information updated successfully."}

    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")



@router.get("", response_model=CompanyListResponseBody, status_code=status.HTTP_200_OK)
async def find_company_list(db: DbDependency):
    """
    会社情報一覧取得
    
    Parameters
    -----------------------
    なし

    Returns
    -----------------------
    companies: array
        company_id: int
            会社のID（int）
        name: str
            会社名
        name_kana: str
            会社名のフリガナ
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        postal_code: str
            郵便番号
        phone_number: str
            電話番号
        email: str
            メールアドレス
        created_at: str
            会社情報が作成された日時（ISO 8601形式）
    
    """
    found_companies = companies_cruds.find_companies(db)
    if not found_companies:
        raise HTTPException(status_code=500, detail="Internal server error.")
    
    companies_list = []
    for company in found_companies:
        di = {
            "company_id": company.id,
            "name": company.name,
            "name_kana": company.name_kana,
            "prefecture": company.prefecture,
            "city": company.city,
            "town": company.town,
            "address": company.address,
            "postal_code": company.postal_code,
            "phone_number": company.phone_number,
            "email": company.email,
            "created_at": company.created_at.isoformat()
        }
        companies_list.append(di)
    
    return {"companies": companies_list}

@router.get("/{company_id}/progresses", response_model=ProgressListResponseBody, status_code=status.HTTP_200_OK)
async def find_progress_list_company(db: DbDependency, company_id: int, name: str = ""):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    検索
        name: str

    Returns
    -----------------------
    progresses: array
        progress_id: int
            進捗のID
        user_id: int
            ユーザーのID
        course_id: int
            コースのID
        section_id: int
            セクションのID
        curriculum_id: int
            カリキュラムのID
        progress_percentage: int
            進捗のパーセンテージ
        status: str
            ステータス
    """

    users = companies_cruds.find_user_by_company_id(db, company_id)
    user_id_list = []
    for user in users:
        if any([
            name and (name in user.first_name),
            name and (name in user.last_name),
            name and (name in user.first_name_kana),
            name and (name in user.last_name_kana),
            name and (name in (user.last_name + user.first_name)),
            name and (name in (user.last_name_kana + user.first_name_kana)),
            name == "" # 検索なし
        ]):
            user_id_list.append(user.id)

    course_progresses = companies_cruds.find_progresses_by_user_id_list(db, user_id_list)
    if not course_progresses:
        raise HTTPException(status_code=404, detail="progresses not found.")

    li = []
    for progress in course_progresses:
        di = {
            "progress_id": progress.id,
            "user_id": progress.user_id,
            "course_id": progress.course_id,
            "section_id": companies_cruds.find_section_by_course_id(db, progress.course_id),
            "curriculum_id": companies_cruds.find_curriculum_by_course_id(db, progress.course_id),
            "progress_percentage": progress.progress_percentage,
            "status": companies_cruds.find_status_by_status_id(db, progress.status_id)
        }
        li.append(di)

    return {"progresses": li}

@router.get("/{company_id}/users", response_model=StudentListResponseBody, status_code=status.HTTP_200_OK)
async def find_student_list_company(db: DbDependency, company_id: int, role: str, page: int, limit: int):
    """
    受講生一覧（法人、法人代行)
    
    Parameters
    -----------------------
    role: str
        ユーザーの役割
    page: int
        取得するページ番号
    limit: int
        1ページ当たりの記事数

    Returns
    -----------------------
    users: array
        user_id: int
            ユーザーのID
        name: str
            ユーザーの名前
        email: str
            ユーザーのメールアドレス
        role: str
            ユーザーのロール
        is_enable: bool
            アカウントの有効状態
        last_login: str
            最終ログイン日（ISO 8601形式）
    """
    users = companies_cruds.find_users_by_company_id_and_role(db, company_id, role)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    
    found_user = []
    for user in users[(page - 1)*limit : page*limit]:
        found_user.append(user)

    return compamies_services.create_users_list(role, found_user)

@router.get("/{company_id}/billings", response_model=BillingListResponseBody, status_code=status.HTTP_200_OK)
async def find_billing_list(db: DbDependency, company_id: int, target_month: str = None, status: str = None):
    """
    請求履歴一覧取得

    Parameter
    -----------------------
    company_id: int
        会社のID
    フィルター
        target_month: str
            (YYYYMM形式)
        status: str

    Returns
    -----------------------
    dict
        billing_id: int
            請求履歴のID
        date: str
            請求日（YYYY-MM-DD形式）
        amount: float
            請求金額
        status: string
            請求状況（例: "paid", "unpaid", "overdue"）
        description:str
            請求内容の説明
    """

    billing_infos = companies_cruds.find_billing_by_company_id(db, company_id)
    if not billing_infos:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    li = []
    info_list = [info.id for info in billing_infos]
    transaction_histories = companies_cruds.find_transaction_histories_by_billing_info_id(db, info_list)
    for history in transaction_histories:
        billing_status = companies_cruds.find_billing_status_by_status_id(db, history.billing_status_id)
        if any([
            target_month and (target_month == history.due_date.strftime("%Y%m")),
            status and (status == billing_status.name),
            (target_month == None) and (status == None) # フィルターなし
        ]):
            di = {
                "billing_id": history.billing_info_id,
                "date": str(history.due_date),
                "amount": history.amount,
                "status": billing_status.name,
                "description": billing_status.description
            }
            li.append(di)

    return {"billings": li}

@router.get("/{company_id}/users/counts", response_model=AccountListResponseBody, status_code=status.HTTP_200_OK)
async def find_number_of_accounts(db: DbDependency, company_id: int):
    """
    有効アカウント数取得(法人、法人代行)
    Parameters
    -----------------------
    company_id: int
        会社のID
    Return
    -----------------------
    company_id: 会社のID
    role_counts: array
        role_id: int
            ロールのID
        role_name: str
            ロールの名称
        count: int
            そのロールを持つ有効なユーザーの数
    """

    company = companies_cruds.find_users_by_company_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    roles = companies_cruds.find_roles(db)
    li = []
    for role in roles:
        users = companies_cruds.find_users_by_role_id(db, role.id)
        di = {
            "role_id": role.id,
            "role_name": role.name,
            "count": len(users)
        }
        li.append(di)

    re_di = {
        "company_id": company.company_id,
        "role_counts": li
    }

    return re_di

@router.post("/{company_id}/billing_info", response_model=CompanyBillingInfoCreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_company_billing_info(db: DbDependency, param: CompanyBillingInfoCreateRequestBody):
    """
    請求先情報作成
    Parameter
    -----------------------
    dict
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        billing_email: str
            メールアドレス
        invoice_number: str
            インボイス番号
        tax_number: str
            タックス番号
        payment_method_id: int
            支払い方法のID
        notes: str
            メモ
        last_receipt_number: str
            領収書番号
    
    Returns
    -----------------------
    dict
        id: int
            請求先情報ID（int）
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        billing_email: str
            メールアドレス
        invoice_number: str
            インボイス番号
        tax_number: str
            タックス番号
        payment_method_id: int
            支払い方法のID
        notes: str
            メモ
        last_receipt_number: str
            領収書番号
    """
    try:
        new_company_billing_info = companies_cruds.create_company_billing_info(db, param)
        db.commit()
        return new_company_billing_info
    
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")

@router.get("/{company_id}/billing_info/{billing_info_id}", response_model=CompanyBillingInfoDetailResponseBody, status_code=status.HTTP_200_OK)
async def find_company_billing_info_details(db: DbDependency, billing_info_id: int = Path(gt=0)):
    """
    請求先情報取得

    Parameter
    -----------------------
    billing_info_id: int
        詳細情報を取得したい請求先情報のID

    Returns
    -----------------------
    dict
        id: int
            請求先情報ID（int）
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        billing_email: str
            メールアドレス
        invoice_number: str
            インボイス番号
        tax_number: str
            タックス番号
        payment_method: str
            支払い方法（例: "クレジットカード", "銀行振り込み" etc...）
        description:str
            支払い方法の説明
        notes: str
            メモ
        last_receipt_number: str
            領収書番号

    """
    company_billing_info = companies_cruds.find_company_billing_info_by_billing_info_id(db, billing_info_id)
    if not company_billing_info:
        raise HTTPException(status_code=404, detail="Company Billing Info not found.")

    return company_billing_info

@router.put("/{company_id}/billing_info/{billing_info_id}", response_model=CompanyBillingInfoUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_company_billing_info(db: DbDependency, update: CompanyBillingInfoUpdateRequestBody, billing_info_id: int = Path(gt=0)):
    """
    会社請求情報更新

    Parameters
    -----------------------
    billing_info_id: int
        更新する請求情報のID
    dict
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        billing_email: str
            メールアドレス
        invoice_number: str
            インボイス番号
        tax_number: str
            タックス番号
        payment_method_id: int
            支払い方法のID
        notes: str
            メモ
        last_receipt_number: str
            領収書番号

    Returns
    -----------------------
    dict
        id: int
            請求先情報ID（int）
        prefecture: str
            都道府県
        city: str
            市区町村
        town: str
            町名、番地等
        address: str
            建物名、部屋番号等
        billing_email: str
            メールアドレス
        invoice_number: str
            インボイス番号
        tax_number: str
            タックス番号
        payment_method_id: int
            支払い方法のID
        notes: str
            メモ
        last_receipt_number: str
            領収書番号
    """
    update_company_billing_info = companies_cruds.update_company_billing_info(db, update, billing_info_id)
    if not update_company_billing_info:
        raise HTTPException(status_code=404, detail="Company Billing Info not found.")

    try:
        db.commit()
        return update_company_billing_info

    except Exception as e:
        logger.error(str(e))
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
