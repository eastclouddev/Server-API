from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query,Request
from sqlalchemy.orm import Session
from starlette import status

from schemas.companies import CreateRequestBody, CreateResponseBody, DetailResponseBody,AllResponseBody,ResponseBody,ProgressesResponseBody
from cruds import companies as companies_cruds
from services import companies as compamies_services

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=CreateResponseBody, status_code=status.HTTP_200_OK)
async def create_company(db: DbDependency, param: CreateRequestBody):
    """
    会社情報作成

    Parameters
    -----------------------
    dict
        name: str
            会社名
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
    


@router.get("/{company_id}", response_model=DetailResponseBody, status_code=status.HTTP_200_OK)
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
    company_info = companies_cruds.find_by_company_id(db, company_id)
    if not company_info:
        raise HTTPException(status_code=404, detail="Company not found.")
    
    info = {
        "company_id": company_id,
        "name": company_info.name,
        "prefecture": company_info.prefecture,
        "city": company_info.city,
        "town": company_info.town,
        "address": company_info.address,
        "postal_code": company_info.postal_code,
        "phone_number": company_info.phone_number,
        "email": company_info.email,
        "created_at": company_info.created_at.isoformat(),
        "updated_at": company_info.updated_at.isoformat()
    }

    return info



@router.get("", response_model=AllResponseBody, status_code=status.HTTP_200_OK)
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
        raise HTTPException(status_code=500,detail="Internal server error.")
    
    companies_list = []

    for company in found_companies:
        one_company = {
            "company_id": company.id,
            "name": company.name,
            "prefecture": company.prefecture,
            "city": company.city,
            "town": company.town,
            "address": company.address,
            "postal_code": company.postal_code,
            "phone_number": company.phone_number,
            "email": company.email,
            "created_at": company.created_at.isoformat()
        }

        companies_list.append(one_company)
    
    return {"companies": companies_list}

@router.get("/{company_id}/progresses",response_model= ProgressesResponseBody,status_code=status.HTTP_200_OK)
async def find_progress_list_company(db: DbDependency, company_id: int):
    """
    進捗管理一覧
    
    Parameters
    -----------------------
    なし

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
    found_course_progresses = companies_cruds.find_course_progresses(db, company_id)


    progresses_list = []

    for progress in found_course_progresses:
        one_progress = {
            "progress_id": progress.id,
            "user_id": progress.user_id,
            "course_id": progress.course_id,
            "section_id": companies_cruds.find_section_id(db,progress.course_id),
            "curriculum_id": companies_cruds.find_curriculum_id(db,progress.course_id),
            "progress_percentage": progress.progress_percentage,
            "status": companies_cruds.find_status_name(db,progress.status_id)
        }

        progresses_list.append(one_progress)

    return {"progresses": progresses_list} 

@router.get("/{company_id}/users", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_student_list_company(db: DbDependency, company_id:int, role: str,  page: int, limit: int):

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
    {"users": users_list} : dic{}
                    受け取ったroleと一致するユーザー全員の情報
    users: array
        user_id: int
            ユーザーのID
        first_name: str
            ユーザーの名
        last_name: str
            ユーザーの姓
        email: str
            ユーザーのメールアドレス
        role: str
            ユーザーのロール
        last_login: str
            最終ログイン日（ISO 8601形式）
    """
    users = companies_cruds.get_user(db, company_id, role)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    
    found_user = []
    for user in users[(page - 1)*limit : page*limit]:
        found_user.append(user)

    return compamies_services.cereate_users_list(role, found_user)