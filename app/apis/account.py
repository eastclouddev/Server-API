from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from logging import getLogger
from typing import Annotated
from database.database import get_db
from schemas.account import ResponseList, ResponseBody
from cruds import account as account_crud
from services import account as account_service



logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="", tags=["AccountList"])



# 受講生一覧（法人、法人代行)
@router.get("/companies/{company_id}/users",response_model=ResponseBody, status_code=status.HTTP_200_OK)

def get_user(db: DbDependency, role: str,  page: int, limit: int):

    """
    受け取ったroleと一致するユーザー全員の情報を取得する
    
    Parameters
    ----------
    role: str,  
        ユーザーの役割
    page: int, 
        取得するページ番号
    limit: int
        1ページ当たりの記事数


    Returns
    -------
    {"users": users_list} : dic{}
                    受け取ったroleと一致するユーザー全員の情報
    
    """

    # found_userにroleが一致するユーザー全員をいれる
    found_user = account_crud.find_by_role(db, role, page, limit)

    if not found_user:

        # found_userになにも入らなかったらstatus_code=404, detail="User not found"を返す
        raise HTTPException(status_code=404, detail="User not found")
    
    # found_userを辞書型に格納
    return  account_service.cereate_users_list(role, found_user)


# 以下同じく
    
# 受講生一覧（メンター）
@router.get("/mentors/{mentor_id}/students", response_model=ResponseBody,status_code=status.HTTP_200_OK)
def get_user(db: DbDependency, role: str, page: int, limit: int):
    found_user = account_crud.find_by_role(db, role, page, limit)

    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return  account_service.cereate_users_list(role, found_user)

# 受講生一覧（管理者）
@router.get("/users",response_model=ResponseBody, status_code=status.HTTP_200_OK)
def get_user(db: DbDependency, role: str, page: int, limit: int):
    found_user = account_crud.find_by_role(db, role, page, limit)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return  account_service.cereate_users_list(role, found_user)


