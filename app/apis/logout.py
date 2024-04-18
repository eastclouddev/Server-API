from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from cruds import logout as logout_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/logout", tags=["Logout"])


@router.post("", status_code=status.HTTP_200_OK)
# async def logout(request: Request):
async def logout(request: Request,db: DbDependency):
    """
    ログアウト機能

    Parameter
    -----------------------
    header
        認証情報が含まれているリクエストヘッダ

    Return
    -----------------------
    なし
    """
    req_headers = dict(request.headers)
    auth = req_headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401,detail="Logout failed.")
    # 'Bearer {access_token}'の"Bearer "の7文字以降のaccess_tokenのみを取得
    access_token = auth[7:]
    user_id = logout_crud.analysis_access_token(access_token)

    if not user_id:
        raise HTTPException(status_code=401,detail="Logout failed.")
    # ログアウト時にデバイス情報の削除
    else:   
        delete_device = logout_crud.delete(db, user_id)
        if not delete_device:
            raise HTTPException(status_code=401,detail="Logout failed.")
        try:
            db.commit()
        except Exception as e:
            logger.error(str(e)) 
            db.rollback()
            raise HTTPException(status_code=400, detail="Deletion data is invalid.") #（仮）

    return