from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

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



def find_question(db:Session,question_id:int):
    found_question = db.query(Questions).filter(Questions.id == question_id).first()

    if not found_question:
        raise HTTPException(status_code=404,detail="Question not found.")

    question = {
        "id":found_question.id,
        "curriculum_id":found_question.curriculum_id,
        "user_id":found_question.user_id,
        "title":found_question.title,
        "content":found_question.content,
        "media_content":found_question.media_content,
        "is_closed":found_question.is_closed,
        "created_at":found_question.created_at.isoformat()
    }
    return question



def find_answers(db:Session,question_id:int):
    return db.query(Answers).filter(Answers.question_id == question_id).all()