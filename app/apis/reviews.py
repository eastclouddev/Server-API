from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from schemas.reviews import RiquestBody,ResponseBody
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from cruds import reviews as review_crud
from logging import getLogger

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/reviews", tags=["ReviewResponses"])


@router.patch("/responses/{response_id}", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def response_update(db: DbDependency, update: RiquestBody,response_id: int = Path(gt=0)):
    try:
        new_response = review_crud.update(db, update,response_id)
        db.commit()
    except Exception as e:
        logger.error(str(e)) # logger.warning,logger.info が使えます
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    return new_response