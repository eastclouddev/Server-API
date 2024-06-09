from sqlalchemy.orm import Session

from schemas.curriculums import QuestionCreateRequestBody

from models.review_requests import ReviewRequests
from models.quiz_contents import QuizContents
from models.questions import Questions
from models.curriculums import Curriculums
from models.users import Users

def find_reviews_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.curriculum_id == curriculum_id).all()

def find_info_by_curriculum_id(db: Session, curriculum_id: int):
    curriculum_info = db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()
    if not curriculum_info:
        return None

    info = {
        "curriculum_id": curriculum_id,
        "title": curriculum_info.title,
        "description": curriculum_info.description,
        "is_test": curriculum_info.is_test,
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

    return info

def find_questions_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(Questions).filter(Questions.curriculum_id == curriculum_id).all()

def find_quiz_contents_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(QuizContents).filter(QuizContents.curriculum_id == curriculum_id).all()

def create_question(db: Session, course_id: int, param: QuestionCreateRequestBody, media_json):
    new_question = Questions(
        curriculum_id = param.curriculum_id,
        course_id = course_id,
        user_id = param.user_id,
        title = param.title,
        objective = param.objective,
        current_situation = param.current_situation,
        research = param.research,
        content = param.content,
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

def find_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()