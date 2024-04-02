from sqlalchemy.orm import Session

from models.questions import Questions 
from models.answers import Answers


def find_by_user_id(db: Session, user_id: int):
    return db.query(Questions).filter(Questions.user_id == user_id).all()

def find_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).first()
