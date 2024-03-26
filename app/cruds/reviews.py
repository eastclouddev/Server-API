from sqlalchemy.orm import Session

from schemas.reviews import CreateRequestBody, RequestBody
from models.users import Users
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses


def create_review_response(db: Session, param:CreateRequestBody, review_request_id: int):
    review_request = db.query(ReviewRequests).filter(ReviewRequests.id == review_request_id)
    if not review_request:
        return None
    
    new_review_response = ReviewResponses(
        review_request_id = review_request_id,
        user_id = param.user_id,
        parent_response_id = param.parent_response_id,
        content = param.content,
        is_read = param.is_read
    )

    db.add(new_review_response)

    return new_review_response
    

def find_response(db: Session, response_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.id == response_id).first()

def update(db: Session, update:RequestBody ,response_id: int):
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