from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.questions import Questions
from models.answers import Answers

from logging import getLogger

logger = getLogger("uvicorn.app")




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
