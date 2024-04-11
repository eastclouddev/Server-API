from sqlalchemy.orm import Session

from models.review_requests import ReviewRequests
from models.curriculums import Curriculums
from models.questions import Questions
from models.curriculums import Curriculums
from models.users import Users

def find_reviews(db: Session, curriculum_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.curriculum_id == curriculum_id).all()

def find_by_curriculum_id(db: Session, curriculum_id: int):
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

def create_question(db: Session, user_id:int, title: str, content: str, media_json, curriculum_id: int):
    new_question = Questions(
        curriculum_id = curriculum_id,
        user_id = user_id,
        title = title,
        content = content,
        media_content = media_json
    )
    db.add(new_question)

    return new_question

def find_curriculum(db: Session, curriculum_id: int):
    return db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()