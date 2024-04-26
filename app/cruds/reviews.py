from sqlalchemy.orm import Session

from schemas.reviews import ReviewResponseUpdateRequestBody, ReviewRequestUpdateRequestBody
from models.users import Users
from models.review_responses import ReviewResponses
from models.review_requests import ReviewRequests
from models.mentorships import Mentorships


def find_response(db: Session, response_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.id == response_id).first()

def update_response(db: Session, update:ReviewResponseUpdateRequestBody ,response_id: int):
    found_response = find_response(db, response_id)
    if not found_response:
        return None
    
    found_response.content = update.content
    found_response.is_read = update.is_read
    db.add(found_response)
    
    update_response = {
        "id": response_id,
        "review_request_id": found_response.review_request_id,
        "user_id": found_response.user_id,
        "parent_response_id": found_response.parent_response_id,
        "content": update.content, 
        "is_read": update.is_read,
        "updated_at": found_response.updated_at.isoformat() 
    }

    return update_response


def find_review(db: Session, review_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.id == review_id).first()


def update_review(db: Session, update:ReviewRequestUpdateRequestBody ,review_id: int):
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

def find_review_request_by_review_request_id(db: Session, review_request_1d: int):
    return db.query(ReviewRequests).filter(ReviewRequests.id == review_request_1d).first()

def find_review_response_by_review_request_id(db:Session, review_request_id:int):
    return db.query(ReviewResponses).filter(ReviewResponses.review_request_id == review_request_id).all()