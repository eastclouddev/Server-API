from sqlalchemy.orm import Session
from sqlalchemy import union_all
from sqlalchemy import desc

from models.questions import Questions
from models.users import Users
from models.answers import Answers
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.notifications import Notifications

def find_notifications_order_by_created_at(db: Session):
    return db.query(Notifications).order_by(desc(Notifications.created_at)).limit(10).all()
    
def find_user_by_id(db: Session, id):
    return db.query(Users).filter(Users.id == id).first()

def update_notificaton_by_id(db: Session, notification_id: int):
    notification = db.query(Notifications).filter(Notifications.id == notification_id).first()
    if not notification:
        return None
    notification.is_read = True
    db.add(notification)

    return notification

def find_question_by_question_id(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_answer_by_answer_id(db: Session, answer_id: int):
    return db.query(Answers).filter(Answers.id == answer_id).first()

def find_request_by_request_id(db: Session, request_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.id == request_id).first()

def find_response_by_response_id(db: Session, response_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.id == response_id).first()
