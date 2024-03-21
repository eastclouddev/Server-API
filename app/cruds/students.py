from sqlalchemy.orm import Session
from models.questions import Questions 
from models.answers import Answers

from logging import getLogger

logger = getLogger("uvicorn.app")


def find_by_question(db: Session,user_id: int):

    questions = db.query(Questions).filter(Questions.user_id == user_id).all()
    
    if not questions:
        return None

    return questions

def cereate_question_list(db,found_question):

    question_list = []

    
    for question in found_question:
        one_question = {
            "id": question.id,
            "title": question.title,
            "content": question.content,
            "curriculum_id": question.curriculum_id,
            "created_at": question.created_at,
            "is_closed": question.is_closed
        }
        answer = db.query(Answers).filter(Answers.question_id == question.id).first()
        find_is_read = {"is_read": answer.is_read }
        one_question.update(find_is_read)

        question_list.append(one_question)

    
    return {"questions": question_list}
    