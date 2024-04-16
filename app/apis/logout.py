from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/logout", tags=["Logout"])


@router.post("", status_code=status.HTTP_200_OK)
async def logout(request: Request):
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

    return