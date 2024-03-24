from sqlalchemy.orm import Session
from models.questions import Questions


def find_by_questions(db: Session, mentor_id: int):
    return db.query(Questions).filter(Questions.user_id == mentor_id).all()