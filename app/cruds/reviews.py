from sqlalchemy.orm import Session
from models.review_requests import ReviewRequests 
from models.review_responses import ReviewResponses
from models.mentorships import Mentorships

from logging import getLogger

logger = getLogger("uvicorn.app")

def find_reviews(db:Session,user_id: int):
    mentorships = db.query(Mentorships).filter(Mentorships.mentor_id == user_id).first()
    return db.query(ReviewRequests).filter(ReviewRequests.user_id == mentorships.student_id).all()

def find_is_read(db:Session,id: int):
    info =  db.query(ReviewResponses).filter(ReviewResponses.review_request_id == id).first()
    if not info:
        return False
    return info.is_read

