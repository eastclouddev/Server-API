from datetime import datetime

from sqlalchemy.orm import Session

from schemas.courses import QuestionCreateRequestBody, ReviewRequestCreateRequestBody
from models.courses import Courses
from models.sections import Sections
from models.curriculums import Curriculums
from models.course_progresses import CourseProgresses
from models.tech_categories import TechCategories
from models.curriculum_progresses import CurriculumProgresses
from models.questions import Questions
from models.answers import Answers
from models.review_requests import ReviewRequests
from models.review_responses import ReviewResponses
from models.users import Users
from models.notifications import Notifications


def find_courses(db: Session):
    return db.query(Courses).all()

def find_course_by_course_id(db: Session, course_id: int):
    return db.query(Courses).filter(Courses.id == course_id).first()

def find_sections_by_course_id(db: Session, course_id: int):
    return db.query(Sections).filter(Sections.course_id == course_id).all()

def find_curriculums_by_section_id(db: Session, section_id: int):
    return db.query(Curriculums).filter(Curriculums.section_id == section_id).all()

def find_course_progress_by_course_id(db: Session, user_id: int, course_id: int):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id, \
                                             CourseProgresses.course_id == course_id).first()

def create_course_progress(db: Session, user_id: int, course_ids: list):
    for course_id in course_ids:
        # 同じレコードが作られないように制限
        if find_course_progress_by_course_id(db, user_id, course_id):
            continue
        course_progress = CourseProgresses(
            user_id = user_id,
            course_id = course_id,
            progress_percentage = 0,
            status_id = 1,
            started_at = datetime.now()
        )
        db.add(course_progress)
    return

def find_course_progress(db: Session, user_id: int, course_ids: list):
    return db.query(CourseProgresses).filter(CourseProgresses.user_id == user_id, \
                                             CourseProgresses.course_id.in_(course_ids)).all()

def find_review_request_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.curriculum_id == curriculum_id).first()

def create_review_request(db: Session, param: ReviewRequestCreateRequestBody, media_json: list, course_id: int):
    new_review = ReviewRequests(
        course_id = course_id,
        curriculum_id = param.curriculum_id,
        user_id = param.user_id,
        title = param.user_id,
        content = param.content,
        media_content = media_json
    )    
    db.add(new_review)

    return new_review

def find_reviews_by_curriculum_id(db: Session, course_id: int):
    return db.query(ReviewRequests).filter(ReviewRequests.course_id == course_id).all()

def find_curriculum_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(Curriculums).filter(Curriculums.id == curriculum_id).first()

def create_question(db: Session, course_id: int, param: QuestionCreateRequestBody, media_json: list):
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

def find_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def find_questions_by_course_id(db: Session, course_id: int):
    return db.query(Questions).filter(Questions.course_id == course_id).all()

def find_notification_by_user_id_and_question_id(db: Session, user_id: int, question_id: int):
    return db.query(Notifications).filter(Notifications.from_user_id == user_id, Notifications.question_id == question_id).all()

def find_notification_by_user_id_and_review_request_id(db: Session, user_id: int, review_request_id: int):
    return db.query(Notifications).filter(Notifications.from_user_id == user_id, Notifications.review_request_id == review_request_id).all()

def find_answers_by_question_id(db: Session, question_id: int):
    return db.query(Answers).filter(Answers.question_id == question_id).all()

def find_response_by_request_id(db: Session, review_request_id: int):
    return db.query(ReviewResponses).filter(ReviewResponses.review_request_id == review_request_id).all()

def find_tech_category_by_category_id(db: Session, tech_category_id: int):
    return db.query(TechCategories).filter(TechCategories.id == tech_category_id).first()

def find_curriculums_by_course_id(db: Session, course_id):
    return db.query(Curriculums).filter(Curriculums.id == course_id).all()

def find_curriculums_progress_by_curriculum_id(db: Session, curriculum_id: int):
    return db.query(CurriculumProgresses).filter(CurriculumProgresses.curriculum_id == curriculum_id).first()