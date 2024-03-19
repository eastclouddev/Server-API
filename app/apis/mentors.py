from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from sqlalchemy.orm import Session
from database.database import get_db
from logging import getLogger


logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/mentors", tags=["Mentors"])

from schemas.mentors import ResponseBody
from cruds import mentors as mentors_crud

@router.get("/{mentor_id}/rewards", response_model=ResponseBody, status_code=status.HTTP_200_OK)
async def find_by_mentor_id(db: DbDependency, mentor_id: int = Path(gt=0)):

    user_rewards = mentors_crud.find_by_mentor_id(db, mentor_id)

    if not user_rewards:
        raise HTTPException(status_code=404, detail="Mentor not found.")

    li = []
    for user_reward in user_rewards:
        di = {
            "reward_id": user_reward.id,
            "date": user_reward.reward_at.strftime("%Y-%m-%d"),
            "amount": user_reward.amount,
            "to_mentor_id": int(mentor_id)
        }
        li.append(di)

    re_di = {
        "rewards": li
    }

    return re_di
