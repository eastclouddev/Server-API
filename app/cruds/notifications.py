from sqlalchemy.orm import Session
from sqlalchemy import union_all
from sqlalchemy import desc

from models.questions import Questions
from models.users import Users
from models.answers import Answers
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses

from models.notifications import Notifications

def find_table(db: Session):
    # 10個制限
    question = db.query(Questions.id, Questions.content, Questions.created_at)\
            .order_by(desc(Questions.created_at)).limit(10)\
        .union_all(db.query(Answers.id, Answers.content, Answers.created_at)\
            .order_by(desc(Answers.created_at)).limit(10))\
        .union_all(db.query(ReviewRequests.id, ReviewRequests.content, ReviewRequests.created_at)\
            .order_by(desc(ReviewRequests.created_at)).limit(10))\
        .union_all(db.query(ReviewResponses.id, ReviewResponses.content, ReviewResponses.created_at)\
            .order_by(desc(ReviewResponses.created_at)).limit(10))\
        .all()
    return question

def find_db(db: Session, id, content, created_at):
    question = db.query(Questions).filter(Questions.id == id, Questions.content == content, Questions.created_at == created_at).first()
    if question:
        return "question", question
    
    answer = db.query(Answers).filter(Answers.id == id, Answers.content == content, Answers.created_at == created_at).first()
    if answer:
        return "answer", answer
    
    request = db.query(ReviewRequests).filter(ReviewRequests.id == id, ReviewRequests.content == content, ReviewRequests.created_at == created_at).first()
    if request:
        return "request", request
    
    response = db.query(ReviewResponses).filter(ReviewResponses.id == id, ReviewResponses.content == content, ReviewResponses.created_at == created_at).first()
    if response:
        return "response", response
    
def find_user_by_id(db: Session, id):
    return db.query(Users).filter(Users.id == id).first()

def update_notificaton_by_id(db: Session, notification_id: int):
    notification = db.query(Notifications).filter(Notifications.id == notification_id).first()
    if not notification:
        return None
    notification.is_read = True
    db.add(notification)

    return notification