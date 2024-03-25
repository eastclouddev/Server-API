from sqlalchemy.orm import Session
from schemas.reviews import RiquestBody
from models.review_responses import ReviewResponses
from fastapi import HTTPException
from models.users import Users

def find_response(db: Session, response_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.id == response_id).first()


def update(db: Session, update:RiquestBody ,response_id: int):
    found_response = find_response(db, response_id)
    if not found_response:
        raise HTTPException(status_code=404, detail="Response not found.")
    
    found_response.content =update.content
    found_response.is_read =update.is_read
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