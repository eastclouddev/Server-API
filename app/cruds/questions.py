from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.users import Users
from models.questions import Questions
from models.answers import Answers
from schemas.questions import RequestBody


def find_by_question(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_by_answer(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).order_by(desc(Answers.id)).first()

def create_answer_parent_answer_id(db: Session, param: RequestBody, question_id: int, answer_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        parent_answer_id = answer_id,
        content = param.content,
    )
    db.add(new_answer)
    return new_answer

def create_answer(db: Session, param: RequestBody, question_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        content = param.content,
    )
    db.add(new_answer)
    return new_answer