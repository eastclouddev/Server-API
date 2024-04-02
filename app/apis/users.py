from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from cruds import users as users_crud
from services import users as users_service

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["AddressUpdate"])

@router.get("/{user_id}/email/confirm_change", status_code=status.HTTP_200_OK)
async def confirm_change_email(token,db: DbDependency, user_id: int = Path(gt=0),):
    """
    メールアドレス認証と更新
    Parameters
    ----------
    user_id: int
        メールアドレスを変更しようとしているユーザーのID
    token: str
        メールアドレス変更を認証するための一意のトークン

    Returns
    -------
    {"message": "Your email address has been successfully updated."}
    
    """
    #一致するユーザーを取得
    found_user = users_crud.find_user(db,user_id)
    if not found_user:
        raise HTTPException(status_code = 400,detail="Invalid or expired token.")
    
    

    #アクセストークンからemailを取得
    token_info = users_service.get_email(token)

    try:
        # 該当のユーザーを更新
        update_info = users_crud.update_address(db,found_user,token_info)
        if not update_info:
            raise HTTPException(status_code = 400,detail="Invalid or expired token.")

        db.commit()
        return {"message": "Your email address has been successfully updated."}

    except Exception as e:
        db.rollback()
        logger.error(e)
        raise HTTPException(status_code= 400,detail="Invalid or expired token.")