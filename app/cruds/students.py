from sqlalchemy.orm import Session

from models.questions import Questions 
from models.answers import Answers
from models.review_requests import ReviewRequests 
from models.review_responses import ReviewResponses

def find_by_user_id(db: Session, user_id: int):
    return db.query(Questions).filter(Questions.user_id == user_id).all()

def find_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).first()

def find_reviews(db:Session, user_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.user_id == user_id).all()

def find_is_read(db:Session, id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.review_request_id == id).all()