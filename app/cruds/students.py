from sqlalchemy.orm import Session

from models.questions import Questions 
from models.answers import Answers


def find_by_question(db: Session,user_id: int):

    found_question = db.query(Questions).filter(Questions.user_id == user_id).all()
    
    if not found_question:
        return None

    return found_question

def cereate_question_list(db: Session, found_question):

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
        if  answer:
            find_is_read = {"is_read": answer.is_read}
            one_question.update(find_is_read)
        else :
            find_is_read = {"is_read": False}
            one_question.update(find_is_read)
        
        question_list.append(one_question)
    
    return {"questions": question_list}
    