from sqlalchemy.orm import Session

from models.learning_statuses import LearningStatuses
from models.questions import Questions
from models.users import Users
from models.answers import Answers
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses

def find_user(db: Session):
    return db.query(Users).first()

def find_questions(db: Session):
    return db.query(Questions).all()

def find_reviews(db:Session):
    return db.query(ReviewRequests).all()

def find_answers(db: Session):
    return db.query(Answers).all()

def find_is_read(db:Session):
    return db.query(ReviewResponses).all()