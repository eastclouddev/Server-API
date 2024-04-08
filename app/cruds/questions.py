from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from models.users import Users
from models.questions import Questions
from models.answers import Answers
from schemas.questions import CreateRequestBody,UpdateQuestioinRequestBody


def find_by_question(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_by_answer(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).order_by(desc(Answers.id)).first()

def create_answer_parent_answer_id(db: Session, param: CreateRequestBody, question_id: int, answer_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        parent_answer_id = answer_id,
        content = param.content,
    )
    db.add(new_answer)
    return new_answer

def create_answer(db: Session, param: CreateRequestBody, question_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        content = param.content,
    )
    db.add(new_answer)
    return new_answer

def find_question(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_answers(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).all()

#####################################
def update_question(db: Session, param: UpdateQuestioinRequestBody, question_id: int):

    question = db.query(Questions).filter(Questions.id == question_id).first()
    if not question:
        return None
    
    question.title = param.title
    question.content = param.content
    question.media_content = param.media_content
    question.is_closed = param.is_closed
    db.add(question)

    return question