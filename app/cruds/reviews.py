from sqlalchemy.orm import Session
from schemas.reviews import RequestBody
from models.review_requests import ReviewRequests
from fastapi import HTTPException
from models.users import Users

def find_review(db: Session, review_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.id == review_id).first()


def update(db: Session, update:RequestBody ,review_id: int):
    found_review = find_review(db, review_id)
    if not found_review:
        return None
    
    found_review.title =update.title
    found_review.content =update.content
    found_review.is_closed =update.is_closed
    db.add(found_review)
    
    update_review = {
        "id": review_id,
        "title": found_review.title,
        "content": found_review.content,
        "is_closed": found_review.is_closed,
        "updated_at": found_review.updated_at.isoformat()
    }

    return update_review