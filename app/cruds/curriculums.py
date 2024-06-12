from sqlalchemy.orm import Session

from models.review_requests import ReviewRequests
from models.quiz_contents import QuizContents
from models.questions import Questions
from models.curriculums import Curriculums
from models.users import Users

def find_reviews_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.curriculum_id == curriculum_id).all()

def find_info_by_curriculum_id(db: Session, curriculum_id: int):
    curriculum_info = db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()
    quiz_contents = db.query(QuizContents).filter(QuizContents.curriculum_id == curriculum_id).all()
    if not curriculum_info:
        return None

    info = {
        "curriculum_id": curriculum_id,
        "title": curriculum_info.title,
        "description": curriculum_info.description,
        "is_quiz": curriculum_info.is_test,
        "display_no": curriculum_info.display_no
    }

    if curriculum_info.video_url:
        find_video_url = {
            "video_url": curriculum_info.video_url
        }
        info.update(find_video_url)

    if curriculum_info.content:
        find_content = {
            "content": curriculum_info.content
        }
        info.update(find_content)

    if curriculum_info.is_test == True:
        for quiz_content in quiz_contents:
            li = []
            di = {
                "quiz_id": quiz_content.id,
                "question": quiz_content.question,
                "media_content": quiz_content.media_content,
                "options": quiz_content.options,
                "correct_answer": quiz_content.correct_answer,
                "explanation": quiz_content.explanation
            }
            li.append(di)

            re_di = {
                "quiz_content": li
            }
            info.update(re_di)

    return info

def find_questions_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(Questions).filter(Questions.curriculum_id == curriculum_id).all()

def find_quiz_contents_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(QuizContents).filter(QuizContents.curriculum_id == curriculum_id).all()

def create_question(db: Session, user_id: int, title: str, content: str, media_json: list, curriculum_id: int):
    new_question = Questions(
        curriculum_id = curriculum_id,
        user_id = user_id,
        title = title,
        content = content,
        media_content = media_json
    )
    db.add(new_question)

    return new_question

def find_curriculum_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()

def find_review_request_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.curriculum_id == curriculum_id).first()

def create_review_request(db: Session, curriculum_id: int, user_id:int, title: str, content: str, is_closed: bool):
    new_review = ReviewRequests(
        curriculum_id = curriculum_id,
        user_id = user_id,
        title = title,
        content = content,
        is_closed = is_closed
    )    
    db.add(new_review)

    return new_review