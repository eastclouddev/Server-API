from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends,Request
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/logout", tags=["logout"])

@router.post("")
async def any_route(request: Request):

    req_headers = dict(request.headers)
    auth = req_headers.get("authorization")
    print(request.headers)
    if not auth:
        raise HTTPException(status_code=401,detail="You are not authorized to perform this action.")

    return {}
