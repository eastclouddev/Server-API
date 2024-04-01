from fastapi import HTTPException, Depends, status, APIRouter,Request
from sqlalchemy.orm import Session
from logging import getLogger
from typing import Annotated
from database.database import get_db
from schemas.reviews import  AllResponseBody
from cruds import reviews as reviews_crud 
from models.mentorships import Mentorships
from models.users import Users

logger = getLogger("uvicorn.app")
DbDependency = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/mentors", tags=["GetAllReviews"])


@router.get("/{mentor_id}/students/reviews",response_model= AllResponseBody,status_code=status.HTTP_200_OK)
async def get_all_reviews(request: Request,db: DbDependency, mentor_id: int):
    """
    受講生のレビュー一覧取得
    
    Parameters
    ----------
    user_id

    Returns
    -------
    {"reviews": reviews_list} : dic{}
                    レビュー一覧
    
    """
    found_reviews = reviews_crud.find_reviews(db,mentor_id)


    reviews_list = []

    for review in found_reviews:
        one_review = {
            "id": review.id,
            "title": review.title,
            "content": review.content,
            "curriculum_id": review.curriculum_id,
            "created_at": review.created_at.isoformat(),
            "is_read": reviews_crud.find_is_read(db,review.id),
            "is_closed": review.is_closed
        }

        reviews_list.append(one_review)

    return {"reviews": reviews_list} 



@router.post("/{mentor_id}/students/reviews")
async def create_mentorship(db: DbDependency, mentor_id: int, student_id: int):
    new_mentorship = Mentorships(
        mentor_id = mentor_id,
        student_id = student_id
    )
    db.add(new_mentorship)
    db.commit()