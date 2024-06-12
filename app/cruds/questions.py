from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from models.users import Users
from models.questions import Questions
from models.answers import Answers

from schemas.questions import AnswerCreateRequestBody, AnswerUpdateRequestBody, QuestionUpdateRequestBody


def find_question_by_question_id(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

def find_answer_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).order_by(desc(Answers.id)).first()

def create_answer_parent_answer_id(db: Session, param: AnswerCreateRequestBody, question_id: int, answer_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        parent_answer_id = answer_id,
        content = param.content,
        media_content = param.media_content
    )
    db.add(new_answer)
    return new_answer

def create_answer(db: Session, param: AnswerCreateRequestBody, question_id: int):
    new_answer = Answers(
        question_id = question_id,
        user_id = param.user_id,
        parent_answer_id = param.parent_answer_id,
        content = param.content,
        media_content = param.media_content
    )
    db.add(new_answer)
    return new_answer

def find_answers_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).all()

def update_question(db: Session, param: QuestionUpdateRequestBody, question_id: int):

    question = db.query(Questions).filter(Questions.id == question_id).first()
    if not question:
        return None
    
    question.title = param.title
    question.content = param.content
    question.media_content = param.media_content
    question.is_closed = param.is_closed
    db.add(question)

    return question

def update_answer(db: Session, param: AnswerUpdateRequestBody, answer_id: int):

    answer = db.query(Answers).filter(Answers.id == answer_id).first()
    if not answer:
        return None
    
    answer.content = param.content
    answer.media_content = param.media_content
    answer.is_read = param.is_read
    db.add(answer)

    return answer

def find_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()
